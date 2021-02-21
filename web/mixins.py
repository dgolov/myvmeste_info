from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View
from .models import Categories, DebitCards, CreditCards, PotrebCredits, MFO, Mortgages, RKO, Refinancing
from profiles.models import Profile, Money, History
import decimal


# Проценты маркетингового плана
PERCENT = [0, 30, 20, 15, 15, 20]


# Content Types моделей офферов
CT_MODEL_MODEL_CLASS = {
        'debetovye-karty': DebitCards,
        'kreditnye-karty': CreditCards,
        'mfo': MFO,
        'potrebitelskie-kredity': PotrebCredits,
        'ipotechnye-kredity': Mortgages,
        'rasschetno-kassovoe-oborudovanie': RKO,
        'refenansirovanie': Refinancing,
    }


class UserMixin(View):

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)


class CategoryDetailMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        if isinstance(self.get_object(), Categories):
            model = CT_MODEL_MODEL_CLASS[self.get_object().slug]
            context = super().get_context_data(**kwargs)
            context['products'] = model.objects.filter(is_active=True).select_related('category')
            return context

        context = super().get_context_data(**kwargs)
        return context


def money_distribution(marketing_money, rest_of_money, first_user, item_user, id, status):
    """ Рекурсивно пробегаемся по 6 уровням участников и пополняем баланс
    :param marketing_money: Деньги в маркетинг
    :param rest_of_money: Остаток денег в маркетинг
    :param first_user: Словарь с информацией об участнике который оформил продукт формируется перед вызовом в mixins.py
                       (Имя Фамилия участника и продукт который он оформил)
    :param item_user: Текущий участник
    :param id: Номер уровня
    :param status: статус заявки
    Пример использования: money_distribution(1000, 1000, user, user, 0, 'подтвержден')
    """
    message = None
    if id == 6:
        return False
    current_status = status
    to_enrollment = marketing_money / 100 * PERCENT[id]
    balance = Money.objects.get(user=item_user)
    if status == 'Ожидает подтверждения':
        if id == 0:
            item_user.profile.set_status()
            item_user.profile.save()
            message = f'Ваша заявка {first_user["offer"]} оформлена.'
            if item_user.profile.status == 0:
                message += f' Вам доступна реферальная ссылка для приглашения новых участников в личном кабинете.'
        balance.under_consideration += decimal.Decimal(to_enrollment)
        if to_enrollment:
            message = f'{first_user["user"]} ({id} уровень). Оформлена заявка: {first_user["offer"]}. <br>' \
                      f'<span style="color: darkgreen; font-weight: bold;">{decimal.Decimal(to_enrollment)}</span> ' \
                      f'руб. на рассмотрении.'
        balance.save()
    elif status == 'Подтвержден':
        if id == 0:
            item_user.profile.set_status(2)
            item_user.profile.save()
            message = f'Ваша заявка {first_user["offer"]} подтверждена. Вам доступна функция вывода денежных средств.'
        balance.under_consideration -= decimal.Decimal(to_enrollment)
        balance.available += decimal.Decimal(to_enrollment)
        if to_enrollment:
            message = f'{first_user["user"]} ({id} уровень). Заявка: {first_user["offer"]} подтверждена. <br>' \
                      f'<span style="color: darkgreen; font-weight: bold;">{decimal.Decimal(to_enrollment)}</span> ' \
                      f'руб. доступно для вывода.'
        balance.save()
    elif status == 'Отклонен':
        if id == 0:
            item_user.profile.set_status()
            item_user.profile.save()
            message = f'Ваша заявка {first_user["offer"]} <span style="color: red;">отклонена</span>.'
        balance.under_consideration -= decimal.Decimal(to_enrollment)
        if to_enrollment:
            message = f'{first_user["user"]} ({id} уровень). Заявка: {first_user["offer"]} отклонена. <br>' \
                      f'<span style="color: red; font-weight: bold;">{decimal.Decimal(to_enrollment)}</span> ' \
                      f'руб. убрано со средств на рассмотрении.'
        balance.save()
    rest_of_money -= to_enrollment
    if message:
        add_to_user_history_list(user=item_user, message=message)
    try:
        # Определение следующего участника (Наставника текущего)
        referral = item_user.profile.referred
        item_user = Profile.objects.get(user=referral)
    except:
        return False
    id += 1
    rest_of_money = marketing_money - to_enrollment
    # Вызов функции со следующим участников
    return money_distribution(marketing_money, rest_of_money, first_user, item_user.user, id, current_status)


def add_to_user_history_list(user, message):
    """ Добаление сообщения в историю пользователя
    :param user: Пользователь
    :param message: Сообщение
    """
    history = History.objects.create(user=user)
    action = f'<b>{history.created_at.strftime("%d-%m-%Y %H:%M")}</b> <br> {message}'
    history.action = action
    history.save()

from profiles.utils import get_product
from web.models import Offers, IDOrders
from profiles.models import Profile, Money, History
import decimal


# Проценты маркетингового плана
PERCENT = [0, 30, 20, 15, 15, 20]


def automatic_report(order_id, user, status, offer_id, is_personal_sale=False):
    """ Парсинг данных взятых по api с партнерских программ
    :param order_id: номер отчета
    :param user: Пользователь
    :param status: Статус заявки
    :param offer_id: Оффер
    :param is_personal_sale: Личная продажа либо обычное оформление оффера
    """
    new_order = False
    try:
        money = Offers.objects.get(offer_id=offer_id)
    except Offers.DoesNotExist:
        return
    try:
        order = IDOrders.objects.get(order_id=order_id)
    except IDOrders.DoesNotExist:
        order = IDOrders.objects.create(user=user.profile, order_id=order_id, offer_id=offer_id, status=status,
                                        broker=user.profile.broker, is_personal_sale=is_personal_sale)
        new_order = True
    offer = get_product(order)
    first_user = {'user': user.get_full_name(), 'offer': offer}
    if not new_order and order.status != status:
        # Отчет уже есть, но статус изменен
        order.status = status
        order.save()
        if order.is_personal_sale:
            distribution_for_personal_sale(user, money.reward, offer, order.status)
        elif order.broker:
            distribution_of_remuneration_50_to_50(first_user, user, money.reward, order.status)
        else:
            money_distribution(marketing_money=money.reward, rest_of_money=money.reward, first_user=first_user,
                               item_user=user, level_struct=0, order=order)
    elif new_order:
        # Отчета нет в системе, создание нового
        if order.is_personal_sale:
            distribution_for_personal_sale(user, money.reward, offer, order.status, new_order=True)
        elif order.broker:
            distribution_of_remuneration_50_to_50(first_user, user, money.reward, order.status, new_order=True)
        else:
            money_distribution(marketing_money=money.reward, rest_of_money=money.reward, first_user=first_user,
                               item_user=user, level_struct=0, order=order, new_order=True)


def make_url_to_leads(user, offer, url):
    """ Генерация ссылки на площадку leads.su
    :param user: Пользователь
    :param offer: Оффер на который нажал пользователь
    :param url: Ссылка в которую подставляются параметры
    :return: Сформированная ссылка
    """
    if user.profile.struct == 1 and url:
        generated_url = url.format(offer.referral_slug, user.profile.pk)
        # message = f'Переход по ссылке на {self.offer}'
        # add_to_user_history_list(self.user, message)
    elif user.profile.struct == 2 and url:
        generated_url = url.format(offer.referral_slug_2, user.profile.pk)
    else:
        generated_url = offer.referral_slug
    return generated_url


def money_distribution(marketing_money, rest_of_money, first_user, item_user, level_struct, order, new_order=False):
    """ Рекурсивно пробегаемся по 6 уровням участников и пополняем баланс
    :param marketing_money: Деньги которые уходят в маркетинг
    :param rest_of_money: Остаток денег в маркетинге
    :param first_user: Словарь с информацией об участнике который оформил продукт формируется перед вызовом в mixins.py
                       (Имя Фамилия участника и продукт который он оформил)
    :param item_user: Текущий участник
    :param level_struct: Номер уровня глубины структуры
    :param order: данные заявки
    :param new_order: Существует ли этот отчет в базе
    Пример использования: money_distribution(1000, 1000, user, user, 0, 'подтвержден')
    """
    message = None
    if level_struct == 6:
        return False
    to_enrollment = marketing_money / 100 * PERCENT[level_struct]
    balance = Money.objects.get(user=item_user)

    if order.status == 'Ожидает подтверждения':
        if level_struct == 0:
            message = f'Ваша заявка {first_user["offer"]} оформлена.'
            if item_user.profile.status == 0:
                message += f' Вам доступна реферальная ссылка для приглашения новых участников в личном кабинете.'
                item_user.profile.set_status()
                item_user.profile.save()
            item_user.profile.save()
            add_an_active_referral(item_user)
        balance.under_consideration += decimal.Decimal(to_enrollment)
        if to_enrollment:
            message = f'{first_user["user"]} ({level_struct} уровень). Оформлена заявка: {first_user["offer"]}. <br>' \
                      f'<span style="color: darkgreen; font-weight: bold;">{decimal.Decimal(to_enrollment)}</span> ' \
                      f'руб. на рассмотрении.'

    elif order.status == 'Подтвержден':
        if level_struct == 0:
            message = f'Ваша заявка {first_user["offer"]} подтверждена.'
            if item_user.profile.status == 1:
                message += ' Вам доступна функция вывода денежных средств.'
                item_user.profile.set_status(2)
                item_user.profile.save()
            item_user.profile.broker = True
            item_user.save()
        add_to_balance(balance, item_user, new_order, to_enrollment)
        if to_enrollment:
            message = f'{first_user["user"]} ({level_struct} уровень). Заявка: {first_user["offer"]} подтверждена.' \
                      f'<br><span style="color: darkgreen; font-weight: bold;">{decimal.Decimal(to_enrollment)}' \
                      f'</span> руб. доступно для вывода.'

    elif order.status == 'Отклонен':
        if level_struct == 0:
            message = f'Ваша заявка {first_user["offer"]} <span style="color: red;">отклонена</span>.'
        if not new_order:
            balance.under_consideration -= decimal.Decimal(to_enrollment)
        if to_enrollment:
            message = f'{first_user["user"]} ({level_struct} уровень). Заявка: {first_user["offer"]} отклонена. <br>' \
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
    except Profile.DoesNotExist:
        return False
    level_struct += 1
    rest_of_money = marketing_money - to_enrollment
    # Рекурсивный вызов функции со следующим участником
    return money_distribution(marketing_money, rest_of_money, first_user, item_user.user, level_struct, order, new_order)


def add_an_active_referral(item_user):
    """ При оформлении заявки пользователем он добавляется в список активных участников к наставнику """
    try:
        referral = Profile.objects.get(pk=item_user.profile.referred.profile.pk)
        referral.active_referrals.add(item_user)
        referral.save()
        if referral.active_referrals.count() >= 3 and referral.broker:
            referral.broker_status = True
            referral.set_status(3)
            referral.save()
    except AttributeError:
        pass


def distribution_of_remuneration_50_to_50(first_user, item_user, marketing_money, status, new_order=False):
    """ После одоброения одной из заявок следующие вознаграждения разделяются 50 на 50 с наставником
        Если пользователь имеет статус брокера, то вызывается данная функция, которая и осуществляет
        разделение 50 на 50
    """
    message = None
    balance = Money.objects.get(user=item_user)
    to_enrollment = marketing_money / 2
    if status == 'Ожидает подтверждения':
        balance.self_under_consideration += decimal.Decimal(to_enrollment)
        message = f' Ваша заявка {first_user["offer"]} оформлена. <span style="color: darkgreen; font-weight: bold;">' \
                  f'{decimal.Decimal(to_enrollment)} </span> руб. личного дохода на рассмотрении.'
    elif status == 'Подтвержден':
        add_to_balance(balance, item_user, new_order, to_enrollment, is_self=True)
        message = f'Ваша заявка {first_user["offer"]} подтверждена.' \
                  f'<br><span style="color: darkgreen; font-weight: bold;">{decimal.Decimal(to_enrollment)}' \
                  f'</span> руб. личного дохода доступно для вывода.'
    elif status == 'Отклонен':
        if not new_order:
            balance.self_under_consideration -= decimal.Decimal(to_enrollment)
        message = f'Ваша заявка {first_user["offer"]} <span style="color: red;">отклонена</span>.<br>' \
                  f'<span style="color: red; font-weight: bold;">{decimal.Decimal(to_enrollment)}</span> ' \
                  f'руб. личного дохода убрано со средств на рассмотрении.'
    balance.save()
    add_to_user_history_list(user=item_user, message=message)
    # Определение наставника и начисление ему половины вознаграждения
    item_user = item_user.profile.referred
    balance = Money.objects.get(user=item_user)
    if status == 'Ожидает подтверждения':
        balance.under_consideration += decimal.Decimal(to_enrollment)
        message = f'{first_user["user"]} (1 уровень). Оформлена заявка: ' \
                  f'{first_user["offer"]}. <br><span style="color: darkgreen; font-weight: bold;">' \
                  f'{decimal.Decimal(to_enrollment)}</span> руб. на рассмотрении.'
    elif status == 'Подтвержден':
        add_to_balance(balance, item_user, new_order, to_enrollment)
        message = f'{first_user["user"]} (1 уровень). Заявка: {first_user["offer"]} подтверждена.' \
                  f'<br><span style="color: darkgreen; font-weight: bold;">{decimal.Decimal(to_enrollment)}' \
                  f'</span> руб. доступно для вывода.'
    elif status == 'Отклонен':
        if not new_order:
            balance.self_under_consideration -= decimal.Decimal(to_enrollment)
        message = f'{first_user["user"]} (1 уровень). Заявка: {first_user["offer"]} отклонена. <br>' \
                  f'<span style="color: red; font-weight: bold;">{decimal.Decimal(to_enrollment)}</span> ' \
                  f'руб. убрано со средств на рассмотрении.'
    balance.save()
    add_to_user_history_list(user=item_user, message=message)


def distribution_for_personal_sale(user, to_enrollment, offer, status, new_order=False):
    """ Зачисление денежных средств при оформлении личных продаж """
    message = None
    balance = Money.objects.get(user=user)
    if status == 'Ожидает подтверждения':
        balance.self_under_consideration += decimal.Decimal(to_enrollment)
        message = f'Оформлена личная продажа: {offer}. <br><span style="color: darkgreen; font-weight: bold;">' \
                  f'{decimal.Decimal(to_enrollment)}</span> руб. личного дохода на рассмотрении.'
    elif status == 'Подтвержден':
        add_to_balance(balance, user, new_order, to_enrollment, is_self=True)
        message = f'Личная продажа: {offer} подтверждена.' \
                  f'<br><span style="color: darkgreen; font-weight: bold;">{decimal.Decimal(to_enrollment)}' \
                  f'</span> руб. личного дохода доступно для вывода.'
    elif status == 'Отклонен':
        if not new_order:
            balance.self_under_consideration -= decimal.Decimal(to_enrollment)
        message = f'Личная продажа: {offer} отклонена. <br>' \
                  f'<span style="color: red; font-weight: bold;">{decimal.Decimal(to_enrollment)}</span> ' \
                  f'руб. личного дохода убрано со средств на рассмотрении.'
    balance.save()
    add_to_user_history_list(user=user, message=message)


def add_to_balance(balance, item_user, new_order, to_enrollment, is_self=False):
    """ Пополнение баланса при статусе заявки 'Одобрено' """
    if is_self:
        if not new_order:
            balance.self_under_consideration -= decimal.Decimal(to_enrollment)
        balance.self_available += decimal.Decimal(to_enrollment)
    else:
        if not new_order:
            balance.under_consideration -= decimal.Decimal(to_enrollment)
        balance.available += decimal.Decimal(to_enrollment)
    if item_user.profile.broker_status:
        balance.sum = balance.available
        balance.sum += balance.self_available
    balance.save()


def add_to_user_history_list(user, message):
    """ Добаление сообщения в историю пользователя
    :param user: Пользователь
    :param message: Сообщение
    """
    history = History.objects.create(user=user)
    action = f'<b>{history.created_at.strftime("%d-%m-%Y %H:%M")}</b> <br> {message}'
    history.action = action
    history.save()

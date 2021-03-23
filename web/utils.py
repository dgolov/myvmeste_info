from profiles.utils import get_product
from web.mixins import money_distribution
from web.models import Offers, IDOrders


def automatic_report(order_id, user, status, offer_id):
    # print(order_id, user.profile.pk, status, offer_id)
    new_order = False
    try:
        money = Offers.objects.get(offer_id=offer_id)
        # print(money.reward)
    except Offers.DoesNotExist:
        return
    try:
        order = IDOrders.objects.get(order_id=order_id)
    except IDOrders.DoesNotExist:
        order = IDOrders.objects.create(
            user=user.profile,
            order_id=order_id,
            offer_id=offer_id,
            status=status,
            broker=user.profile.broker
        )
        new_order = True
    if not new_order and order.status != status:
        # Отчет уже есть, но статус изменен
        order.status = status
        order.save()
        first_user = {'user': user.get_full_name(), 'offer': get_product(order)}
        money_distribution(marketing_money=money.reward, rest_of_money=money.reward,
                           first_user=first_user, item_user=user, level_struct=0, order=order)
    elif new_order:
        # Отчета нет в системе, создание нового
        first_user = {'user': user.get_full_name(), 'offer': get_product(order)}
        money_distribution(marketing_money=money.reward, rest_of_money=money.reward,
                           first_user=first_user, item_user=user, level_struct=0, order=order)


def make_url_to_leads(user, offer, url):
    if user.profile.struct == 1 and url:
        generated_url = url.format(offer.referral_slug, user.profile.pk)
        # message = f'Переход по ссылке на {self.offer}'
        # add_to_user_history_list(self.user, message)
    elif user.profile.struct == 2 and url:
        generated_url = url.format(offer.referral_slug_2, user.profile.pk)
    else:
        generated_url = offer.referral_slug
    return generated_url

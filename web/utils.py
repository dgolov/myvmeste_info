from profiles.utils import get_product
from web.mixins import money_distribution
from web.models import Offers, IDOrders


def automatic_report(order_id, user, status, offer_id):
    # print(order_id, user, status, offer_id)
    new_order = False
    try:
        money = Offers.objects.get(offer_id=offer_id)
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

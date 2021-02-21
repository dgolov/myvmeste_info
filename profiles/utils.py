import os
import qrcode
from django.contrib.auth.models import User
from django.core.files.base import File
from django.http import Http404, HttpResponseRedirect
from myvmeste import settings
from .models import ReferralCodes
from web.models import Offers, DebitCards, CreditCards, PotrebCredits, Mortgages, Refinancing, MFO, RKO


def get_referred_user(request):
    """ Определение реферала (Пригласившего пользователя)
    """
    try:
        referred_user = User.objects.get(username=request.session['referral'])
    except:
        referred_user = None
    return referred_user


def create_referral_struct(user, new_user, struct_id):
    if struct_id == 1:
        user.profile.struct1.add(new_user)
    elif struct_id == 2:
        user.profile.struct2.add(new_user)
    elif struct_id == 3:
        user.profile.struct3.add(new_user)
    elif struct_id == 4:
        user.profile.struct4.add(new_user)
    elif struct_id == 5:
        user.profile.struct5.add(new_user)
    user.profile.save()
    if user.profile.referred and struct_id < 5:
        struct_id += 1
        create_referral_struct(user.profile.referred, new_user, struct_id)


def generate_qr(request):
    if not request.user:
        raise Http404("Poll does not exist")
    code = ReferralCodes.objects.get(user=request.user)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    data = f'http://myvmeste.info?r={code.code}'
    qr.add_data(data)
    qr.make(fit=True)
    filename = f'{code.code}.png'
    img = qr.make_image()
    path = os.path.join(settings.MEDIA_ROOT, 'qr_code', 'temp', filename)
    img.save(path)
    destination_file = open(path, 'rb')
    code.qr_code.save(filename, File(destination_file), save=False)
    destination_file.close()
    code.save()
    img.close()
    os.remove(path)
    return HttpResponseRedirect('/profile')


def get_product(order):
    product_name = None
    offer = Offers.objects.get(offer_id=order.offer_id)

    if offer.category.name == 'Дебетовые карты':
        product = DebitCards.objects.get(offer_id=order.offer_id)
        product_name = f'{offer.category.name} - "{product.card_name}"'
    elif offer.category.name == 'Кредитные карты':
        product = CreditCards.objects.get(offer_id=order.offer_id)
        product_name = f'{offer.category.name} - "{product.card_name}"'
    elif offer.category.name == 'Потребительские кредиты':
        product = PotrebCredits.objects.get(offer_id=order.offer_id)
        product_name = f'{offer.category.name} - "{product.bank_name}"'
    elif offer.category.name == 'Ипотечные кредиты':
        product = Mortgages.objects.get(offer_id=order.offer_id)
        product_name = f'{offer.category.name} - "{product.bank_name}"'
    elif offer.category.name == 'Рефинансирование':
        product = Refinancing.objects.get(offer_id=order.offer_id)
        product_name = f'{offer.category.name} - "{product.bank_name}"'
    elif offer.category.name == 'МФО':
        product = MFO.objects.get(offer_id=order.offer_id)
        product_name = f'{offer.category.name} - "{product.bank_name}"'
    elif offer.category.name == 'Рассчетно кассовое обслуживание':
        product = RKO.objects.get(offer_id=order.offer_id)
        product_name = f'{offer.category.name} - "{product.bank_name}"'

    return product_name

from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import date
from profiles.models import Profile
import requests
from web.utils import automatic_report


API_LEADS_CONF = {
    # http://api.leads.su/webmaster/conversions?start_date=2014-02-01&end_date=2014-02-20&offset=847&token=YOUR_TOKEN
    'url': 'http://api.leads.su/webmaster/conversions',
    'status': {
        'pending': 'Ожидает подтверждения',
        'approved': 'Подтвержден',
        'rejected ': 'Отклонен'
    }
}

API_GURU_CONF = {
    # https://api.guruleads.ru/1.0/stats/conversions?access-token=YOUR_TOKEN&date_start=DATE&date_end=DATE
    'token': 'ca917561b32c1620512547d9ca8be01d',
    'url': 'https://api.guruleads.ru/1.0/stats/conversions',
    'status': {
        2: 'Ожидает подтверждения',
        1: 'Подтвержден',
        3: 'Отклонен',
    },
    'offers': {
        # На разных площадках офферы имеют разные id. Здесь подбивается под одно
        # Райф
        541: 9385,
        # Росбанк
        435: 8836,
        # Восточный
        398: 9483,
    }
}

end_date = date.today()


@shared_task
def get_reports_from_debit_leads_task():
    """ Получение отчета с партнерской программы leads.su из кабинета с дебетовыми картами
    """
    token = 'ed8d9b747dd38505c298310009c45a3f'
    get_leads_reports(token=token)


@shared_task
def get_reports_from_credit_leads_task():
    """ Получение отчета с партнерской программы leads.su из кабинета с кредитными картами
    """
    token = '748af342bf59219c186b487f14c42c81'
    get_leads_reports(token=token)


@shared_task
def get_reports_from_mfo_leads_task():
    """ Получение отчета с партнерской программы leads.su из кабинета с МФО
    """
    token = 'ced4854fb6f47ffb82d0f7e100956f28'
    get_leads_reports(token=token)


def get_leads_reports(token):
    """ Получение отчета с партнерской программы leads.su
        ОБЩАЯ ЛОГИКА ЗАПРОСА
    """
    month = f'0{end_date.month}' if int(end_date.month) < 10 else f'{end_date.month}'
    response = requests.get(
        f"{API_LEADS_CONF['url']}?start_date={end_date.year}-{month}-01&end_date={end_date}&token={token}&limit=500"
    )
    for conversion in response.json()['data']:
        try:
            if conversion['aff_sub1']:
                user = Profile.objects.get(pk=conversion['aff_sub1'])
                is_personal_sale = False
            else:
                user = Profile.objects.get(pk=conversion['aff_sub2'])
                is_personal_sale = True
            order_id = conversion['id']
            conversion_status = conversion['status']
            status = API_LEADS_CONF['status'][conversion_status]
            offer_id = conversion['offer_id']
            automatic_report(order_id, user.user, status, offer_id, is_personal_sale)
        except:
            continue


@shared_task
def get_reports_from_guru_task():
    """ Получение отчета с партнерской программы guruleads.ru
    """
    response = requests.get(
        f"{API_GURU_CONF['url']}?access-token={API_GURU_CONF['token']}&date_start=2021-03-16&date_end={end_date}")
    for conversion in response.json()['data']['items']:
        try:
            if conversion['sub1']:
                user = Profile.objects.get(pk=conversion['sub1'])
                is_personal_sale = False
            else:
                user = Profile.objects.get(pk=conversion['sub2'])
                is_personal_sale = True
            order_id = conversion['external_id']
            conversion_status = conversion['status']
            status = API_GURU_CONF['status'][conversion_status]
            offer_id = API_GURU_CONF['offers'][conversion['offer_id']]
            automatic_report(order_id, user.user, status, offer_id, is_personal_sale)
        except:
            continue

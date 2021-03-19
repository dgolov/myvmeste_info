from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import date
from profiles.models import Profile
import requests
from web.utils import automatic_report


API_LEADS_CONF = {
    # http://api.leads.su/webmaster/conversions?start_date=2014-02-01&end_date=2014-02-20&offset=847&token=YOUR_TOKEN
    'token': 'ed8d9b747dd38505c298310009c45a3f',
    'url': 'http://api.leads.su/webmaster/conversions',
    'status': {
        'pending': 'Ожидает подтверждения',
        'approved': 'Подтвержден',
        'rejected ': 'Отклонен'
    }
}

API_GURU_CONF = {
    # https://api.guruleads.ru/1.0/stats/conversions?access-token=YOUR_TOKEN&date_start=DATE&date_end=DATE
    'tocken': 'ca917561b32c1620512547d9ca8be01d',
    'url': 'https://api.guruleads.ru/1.0/stats/conversions',
    'status': {
        2: 'Ожидает подтверждения',
        1: 'Подтвержден',
        3: 'Отклонен',
    },
    'offers': {
        # На разных площадках офферы имеют разные id. Здесь подбивается под одно
        541: 9385
    }
}

end_date = date.today()


@shared_task
def get_reports_from_debit_leads_task():
    response = requests.get(
        f"{API_LEADS_CONF['url']}?start_date=2021-02-01&end_date={end_date}&token={API_LEADS_CONF['token']}"
    )
    for conversion in response.json()['data']:
        try:
            user = Profile.objects.get(pk=conversion['aff_sub1'])
            order_id = conversion['id']
            conversion_status = conversion['status']
            status = API_LEADS_CONF['status'][conversion_status]
            offer_id = conversion['offer_id']
            automatic_report(order_id, user.user, status, offer_id)
        except:
            continue


@shared_task
def get_reports_from_guru_task():
    response = requests.get(
        f"{API_GURU_CONF['url']}?access-token={API_GURU_CONF['tocken']}&date_start=2021-03-16&date_end={end_date}")
    for conversion in response.json()['data']['items']:
        try:
            user = Profile.objects.get(pk=conversion['sub1'])
            order_id = conversion['external_id']
            conversion_status = conversion['status']
            status = API_GURU_CONF['status'][conversion_status]
            offer_id = API_GURU_CONF['offers'][conversion['offer_id']]
            automatic_report(order_id, user.user, status, offer_id)
        except:
            continue

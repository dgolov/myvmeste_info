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


@shared_task
def my_first_task():
    end_date = date.today()
    # response = requests.get(
    #     f"{API_LEADS_CONF['url']}?start_date=2021-02-01&end_date={end_date}&token={API_LEADS_CONF['token']}"
    # )
    # for conversion in response.json()['data']:
    #     try:
    #         user = Profile.objects.get(pk=conversion['aff_sub1'])
    #         order_id = conversion['id']
    #         conversion_status = conversion['status']
    #         status = API_LEADS_CONF['status'][conversion_status]
    #         print(status)
    #         offer_id = conversion['offer_id']
    #         automatic_report(order_id, user.user, status, offer_id)
    #     except:
    #         continue

    resp = {
        'status': 'success',
        'data': {
            'items': [
                {
                    'hash': 'f6976d90b1e586dc67ab2f65ff00faaf',
                    'offer_id': 541,
                    'offer_name': 'Райффайзен Банк -Дебетовая карта Кэшбек (Приват)',
                    'user_ip': '176.59.99.91', 'os': 'iPhone', 'browser': 'Safari',
                    'status': 2, 'payment': '1870.0000', 'currency_code': 'RUB',
                    'goal_name': 'Активация + Транзакция', 'source': '',
                    'sub1': '63',
                    'sub2': '', 'sub3': '', 'sub4': '', 'sub5': '', 'sub6': '', 'sub7': '',
                    'sub8': '', 'sub9': '', 'sub10': '', 'referrer': '',
                    'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
                    'notice': '', 'external_id': '13187100',
                    'date_time': '2021-03-16 05:50:32', 'approved_at': None
                }
            ],
            '_links': {
                'self': {
                    'href': 'https://api.guruleads.ru/1.0/stats/conversions?access-token=ca917561b32c1620512547d9ca8be01d&date_start=2021-03-16&date_end=2021-03-16&page=1&page_size=100'
                }
            },
            '_meta': {'totalCount': 1, 'pageCount': 1, 'currentPage': 1, 'perPage': 100}
        }
    }

    response = requests.get(
        f"{API_GURU_CONF['url']}?access-token={API_GURU_CONF['tocken']}&date_start=2021-03-16&date_end={end_date}")
    # print(response.json())
    print('start')
    for conversion in response.json()['data']['items']:
        try:
            user = Profile.objects.get(pk=conversion['sub1'])
            print(user)
            order_id = conversion['external_id']
            print(order_id)
            conversion_status = conversion['status']
            status = API_GURU_CONF['status'][conversion_status]
            print(status)
            offer_id = API_GURU_CONF['offers'][conversion['offer_id']]
            print(offer_id)
            automatic_report(order_id, user.user, status, offer_id)
        except:
            continue

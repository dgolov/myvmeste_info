from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import date
from profiles.models import Profile
import requests
from web.utils import automatic_report

TOKEN = '9dc4f54100c92ce9f89b6bfff310f682'
URL = 'http://api.leads.su'
LEADS_STATUS = {'pending': 'Ожидает подтверждения', 'approved': 'Подтвержден', 'rejected ': 'Отклонен'}
today = date.today()

@shared_task
def my_first_task():
    response = requests.get(f'{URL}/webmaster/conversions?start_date=2021-02-01&end_date={today}&token={TOKEN}')
    for conversion in response.json()['data']:
        try:
            user = Profile.objects.get(pk=conversion['aff_sub1'])
            order_id = conversion['id']
            status = LEADS_STATUS[conversion['status']]
            offer_id = conversion['offer_id']
            automatic_report(order_id, user.user, status, offer_id)
        except:
            continue
    print('This is my first task!')


@shared_task
def add(x, y):
    return x + y

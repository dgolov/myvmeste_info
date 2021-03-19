import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myvmeste.settings')

app = Celery('myvmeste')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'reports-from-debit-leads': {
        'task': 'web.tasks.get_reports_from_debit_leads_task',
        'schedule': 180.0,
    },
    'reports-from-credit-leads': {
        'task': 'web.tasks.get_reports_from_credit_leads_task',
        'schedule': 180.0,
    },
    'reports-from-mfo-leads': {
        'task': 'web.tasks.get_reports_from_mfo_leads_task',
        'schedule': 180.0,
    },
    'reports-from-guru': {
        'task': 'web.tasks.get_reports_from_guru_task',
        'schedule': 180.0,
    },
}

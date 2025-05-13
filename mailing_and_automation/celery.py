# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'winston.settings')

app = Celery('yourproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Schedule the email campaign task to run every hour
app.conf.beat_schedule = {
    'send-drip-campaigns-hourly': {
        'task': 'yourapp.tasks.send_drip_campaign_emails',
        'schedule': crontab(minute=0),  # Run at the top of every hour
    },
}
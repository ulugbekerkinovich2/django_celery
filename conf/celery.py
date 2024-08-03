from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Make sure the Django settings module is correctly set.
# This should point to the settings.py file of your Django project.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')  # Replace 'conf' with your actual project name.

# Initialize a Celery application.
# The first argument 'conf' should match the name of your Django project if possible.
app = Celery('conf')

# Load configuration from Django settings.
# The namespace 'CELERY' means Celery settings must be prefixed with 'CELERY_' in your Django settings file.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks from all applications in your INSTALLED_APPS list.
app.autodiscover_tasks()

# Define a simple debug task to verify requests.
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# Configure the beat schedule within the Celery application instance.
print("Configuring the beat schedule...")
app.conf.beat_schedule = {
    'fetch_data_every_2_minutes': {
        'task': 'basic_app.tasks.fetch_and_save_data',  # Ensure this path matches where the task is defined in your Django project.
        'schedule': crontab(minute='*/2'),  # This task will execute every 2 minutes.
    },
}

# If 'basic_app.tasks.fetch_and_save_data' does not exist, you'll get errors. Ensure the task is defined in basic_app/tasks.py

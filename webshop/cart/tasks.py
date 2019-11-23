from celery.schedules import crontab
from celery.task import periodic_task
from django.utils import timezone
from .models import Order


@periodic_task(run_every=crontab(minute='*/5'))
def delete_old_orders():
    orders = Order.objects.filter(is_confirmed=False)
    for order in orders:
        if order.expiration_date < timezone.now():
            order.delete()
    print("completed deleting foos at {}".format(timezone.now()))
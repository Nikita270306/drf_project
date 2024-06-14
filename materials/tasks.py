from datetime import timezone

from celery import shared_task
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from users.models import User


@shared_task
def send_course_update_email(email):
    subject = 'Обновление курса'
    message = 'Здравствуйте! Мы рады сообщить вам о том, что материалы курса были обновлены.'
    send_mail(subject, message, EMAIL_HOST_USER, [email])

@shared_task
def check_inactive_users():
    one_month_ago = timezone.now() - timezone.timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago)
    for user in inactive_users:
        user.is_active = False
        user.save()

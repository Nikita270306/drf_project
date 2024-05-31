from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=200, unique=True, verbose_name='Электронная почта')
    phone = models.CharField(max_length=35, verbose_name='phone number', null=True, blank=True)
    country = models.CharField(max_length=100, verbose_name='country', null=True, blank=True)
    is_password_reset = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=8)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method_choices = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]
    payment_method = models.CharField(max_length=10, choices=payment_method_choices)
    stripe_id = models.CharField(max_length=300, verbose_name='stripe_id', blank=True, null=True)

    def __str__(self):
        return f"Payment: {self.user}, {self.payment_date}, {self.amount}"


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'course']

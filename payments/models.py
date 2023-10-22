from django.conf import settings
from django.db import models

from lessons.models import Course, Lesson

NULLABLE = {'null': True, 'blank': True}


class Payment(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Наличные'),
        ('Remittance', 'Перевод')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь',
                             **NULLABLE)
    payment_date = models.DateField(auto_now_add=True, verbose_name='дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name='оплаченный курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, verbose_name='оплаченный урок', **NULLABLE)
    amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES,
                                      verbose_name='способ оплаты')

    def __str__(self):
        return f'{self.course if self.course else self.lesson} ({self.payment_date})'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'

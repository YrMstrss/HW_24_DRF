from django.core.management import BaseCommand

from payments.models import Payment


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        payment = Payment.objects.create(
            user_id=1,
            course_id=1,
            amount=20000,
            payment_method='Cash'
        )
        payment.save()

        payment = Payment.objects.create(
            user_id=1,
            lesson_id=3,
            amount=3000,
            payment_method='Remittance'
        )
        payment.save()

        payment = Payment.objects.create(
            user_id=2,
            course_id=1,
            amount=20000,
            payment_method='Remittance'
        )
        payment.save()

        payment = Payment.objects.create(
            user_id=2,
            lesson_id=3,
            amount=3000,
            payment_method='Cash'
        )
        payment.save()

        payment = Payment.objects.create(
            user_id=2,
            lesson_id=4,
            amount=3000,
            payment_method='Cash'
        )
        payment.save()


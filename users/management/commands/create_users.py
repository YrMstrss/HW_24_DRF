from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user_1 = User.objects.create(
            email='ivan@ivanov.com',
            first_name='Ivan',
            last_name='Ivanov',
            phone='88005553535',
            city='Moscow'
        )

        user_1.set_password('Ivanov123')
        user_1.save()

        user_2 = User.objects.create(
            email='petr@petrov.com',
            first_name='Petr',
            last_name='Petrov',
            phone='89998887766',
            city='St.Petersburg'
        )

        user_2.set_password('Petrov321')
        user_2.save()

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from lessons.models import Course
from users.models import User


class LessonCreateTestCase(APITestCase):
    """Тест кейс на создание нового урока"""
    def setUp(self) -> None:

        self.client = APIClient()

        self.user = User.objects.create(
            email='ivan@ivanov.com',
            first_name='Ivan',
            last_name='Ivanov',
            phone='88005553535',
            city='Moscow'
        )
        self.user.set_password('Ivanov123')
        self.user.save()

        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='Course test',
            description='Course description'
        )

    def test_create_lesson(self):

        data = {
            'title': 'Test lesson',
            'description': 'Test description',
            'video_link': 'https://www.youtube.com/test',
            'course': self.course.id
        }

        responce = self.client.post(
            reverse('lessons:create-lesson'),
            data=data
        )

        self.assertEqual(
            responce.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            responce.json(),
            {
                "id": 1,
                "title": "Test lesson",
                "preview": None,
                "description": "Test description",
                "video_link": "https://www.youtube.com/test",
                "course": 1,
                "owner": 1
            }
        )

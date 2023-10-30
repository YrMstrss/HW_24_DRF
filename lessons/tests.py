from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from lessons.models import Course, Lesson, Subscription
from lessons.serializers import LessonSerializer
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


class LessonReadTestCase(APITestCase):
    """Тест кейс на чтение записи об уроках"""
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

        self.lesson_1 = Lesson.objects.create(
            title='Test lesson 1 read',
            description='Test description 1 read',
            video_link='https://www.youtube.com/test_1_read',
            course=self.course,
            owner=self.user
        )

        self.lesson_2 = Lesson.objects.create(
            title='Test lesson 2 read',
            description='Test description 2 read',
            video_link='https://www.youtube.com/test_2_read',
            course=self.course
        )

    def test_read_lesson_list(self):
        """Тест на чтение списка уроков"""
        responce = self.client.get(
            reverse('lessons:list-lesson'),
        )

        self.assertEqual(
            responce.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            responce.json(),
            {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 1,
                        "title": "Test lesson 1 read",
                        "preview": None,
                        "description": "Test description 1 read",
                        "video_link": "https://www.youtube.com/test_1_read",
                        "course": 1,
                        "owner": 1
                    },
                    {
                        "id": 2,
                        "title": "Test lesson 2 read",
                        "preview": None,
                        "description": "Test description 2 read",
                        "video_link": "https://www.youtube.com/test_2_read",
                        "course": 1,
                        "owner": None
                    }
                ]
            }
        )

    def test_read_single_lesson(self):
        """Тест на чтение одного урока"""
        responce = self.client.get(
            reverse('lessons:view-lesson', args=[self.lesson_1.id]),
        )

        self.assertEqual(
            responce.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            responce.json(),
            {
                "id": 1,
                "title": "Test lesson 1 read",
                "preview": None,
                "description": "Test description 1 read",
                "video_link": "https://www.youtube.com/test_1_read",
                "course": 1,
                "owner": 1
            }
        )


class LessonUpdateTestCase(APITestCase):
    """Тест кейс на изменение записи об уроках"""
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

        self.lesson = Lesson.objects.create(
            title='Test lesson update',
            description='Test description update',
            video_link='https://www.youtube.com/test_update',
            course=self.course,
            owner=self.user
        )

        self.data = LessonSerializer(self.lesson).data
        self.data.update({
            'title': 'Test lesson UPDATE',
            'description': 'Test description UPDATE',
            'video_link': 'https://www.youtube.com/test_UPDATE',
            'course': self.course.id,
            'owner': self.user.id,
            'preview': ''
        })

    def test_put_lesson(self):
        """Тест для полного изменения урока"""

        response = self.client.put(
            reverse('lessons:edit-lesson', args=[self.lesson.id]),
            self.data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


class LessonDeleteTestCase(APITestCase):
    """Тест кейс на удаление записи об уроках"""
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

        self.lesson = Lesson.objects.create(
            title='Test lesson delete',
            description='Test description delete',
            video_link='https://www.youtube.com/test_delete',
            course=self.course,
            owner=self.user
        )

    def test_delete_lesson(self):

        response = self.client.delete(
            reverse('lessons:delete-lesson', args=[self.lesson.id])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class SubscriptionCreateTestCase(APITestCase):
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

    def test_create_subscription(self):

        data = {
            'course': self.course.id
        }

        responce = self.client.post(
            reverse('lessons:get-subscription'),
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
                "user": 1,
                "course": 1,
                "is_active": True
            }
        )


class SubscriptionDeleteTestCase(APITestCase):
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

        self.subscription = Subscription.objects.create(
            course=self.course,
            user=self.user
        )

    def test_delete_lesson(self):

        response = self.client.delete(
            reverse('lessons:delete-subscription', args=[self.subscription.id])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
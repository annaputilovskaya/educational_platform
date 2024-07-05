from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription
from users.models import User


class CourseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@example.com")
        self.course = Course.objects.create(
            title="Test Course",
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("title"), self.course.title
        )

    def test_course_create(self):
        url = reverse("lms:course-list")
        data = {
                "title": "Test Course 2",
            }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Course.objects.last().title, data.get("title")
        )

    def test_course_update(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))
        data = {"title": "Updated Test Course"}
        response = self.client.patch(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            Course.objects.get(pk=self.course.pk).title, data.get("title")
        )

    def test_course_delete(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertFalse(Course.objects.all().count(), 0)

    def test_course_list(self):
        url = reverse("lms:course-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {'id': self.course.pk,
                 'count_lessons': 0,
                 'lessons': [],
                 'subscription': False,
                 'title': self.course.title,
                 'preview': None,
                 'description': None,
                 'owner': self.user.pk
                 }
            ]
        }

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(data, result)


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@example.com")
        self.course = Course.objects.create(
            title="Test Course",
            owner=self.user,
        )
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            video_link="https://youtube.com/video",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("lms:lesson", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("title"), self.lesson.title
        )

    def test_lesson_create(self):
        url = reverse("lms:lesson-create")
        data = {
                "title": "Test Lesson 2",
                "video_link": "https://youtube.com/video",
                "course": self.course.pk,
            }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.count(), 2
        )

    def test_lesson_create_validation_error(self):
        url = reverse("lms:lesson-create")
        data = {
                "title": "Test Lesson 2",
                "video_link": "https://my.sky.pro",
                "course": self.course.pk,
            }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_lesson_update(self):
        url = reverse("lms:lesson-update", args=(self.lesson.pk,))
        data = {
                "title": "Updated Test Lesson",
                "video_link": "https://youtube.com/video_updated",
                "course": self.course.pk,
            }
        response = self.client.patch(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            Lesson.objects.get(pk=self.lesson.pk).title, data.get("title")
        )

    def test_lesson_delete(self):
        url = reverse("lms:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.count(), 0
        )

    def test_lesson_list(self):
        url = reverse("lms:lesson-list")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            len(data.get("results")), Lesson.objects.count()
        )


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@example.com")
        self.course = Course.objects.create(
            title="Test Course",
            owner=self.user,
        )
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        Subscription.objects.all().delete()
        url = reverse("lms:subscription")
        data = {
                "course": self.course.pk,
            }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            Subscription.objects.all()[0].course, self.course
        )

    def test_subscription_delete(self):
        url = reverse("lms:subscription")
        response = self.client.post(url, {"course": self.course.pk})
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            Subscription.objects.count(), 0
        )

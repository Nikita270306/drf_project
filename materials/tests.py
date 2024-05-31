import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from materials.models import Course, Lesson
from users.models import User

class LessonCRUDTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='admin', email='admin@gmail.com', password='12345')
        self.course = Course.objects.create(title='Test Course', description='This is a test course')
        self.client.force_authenticate(user=self.user)
        self.lesson = Lesson.objects.create(title='Test Lesson', course=self.course, owner=self.user)

    def test_lesson_create(self):
        url = reverse("materials:lesson-create")
        data = {
            'title': 'English lessons',
            'description': 'English with confidence',
            'video_link': 'https://www.youtube.com/watch?v=2To6EqvVPYo',
            'course': self.course.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.filter(title='English lessons').exists())
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_retrieve(self):
        url = reverse("materials:lesson-get", args=[self.lesson.pk])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['title'], self.lesson.title)
        self.assertEqual(data['id'], self.lesson.pk)
        self.assertEqual(data['description'], self.lesson.description)

    def test_lesson_update(self):
        url = reverse("materials:lesson-update", args=[self.lesson.pk])
        data = {
            'title': 'Russian lessons',
            'description': 'Russian with confidence',
            'video_link': 'https://www.youtube.com/watch?v=2To6EqvVPYo',
            'course': self.course.id
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['title'], "Russian lessons")

    def test_lesson_delete(self):
        url = reverse("materials:lesson-delete", args=[self.lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lesson-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
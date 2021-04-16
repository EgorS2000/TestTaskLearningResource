from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token


class CreateQuizTests(APITestCase):
    def test_case(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(
            username='admin',
            password='admin'
        )
        self.token = Token.objects.create(user=self.user)
        data = {
            "question": "How are you?",
            "answers": [
                "Nice",
                "Good",
                "Bad"
            ]
        }

        response = self.client.post(
            reverse('create_quiz'),
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def give_answer_test_case(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(
            username='user',
            password='_12345678_'
        )
        self.token = Token.objects.create(user=self.user)
        data = {
            "answers": [
                "Nice",
                "Good"
            ]
        }

        response = self.client.post(
            reverse('give_quiz_answer'),
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

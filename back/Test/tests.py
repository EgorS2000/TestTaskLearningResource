from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token


class CreateTestTests(APITestCase):
    def test_case(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(
            username='admin',
            password='admin'
        )
        self.token = Token.objects.create(user=self.user)
        data = {
            "name": "Summary",
            "deadline": "21/04/2021 23:50:00",
            "sphere": "IT",
            "questions":
                {
                    "1+2": {
                        "3": True,
                        "5": False,
                        "10": False
                    },
                    "5+5": {
                        "10": True,
                        "15": False,
                        "20": False
                    }
                },
            "questions_value": [5, 5]
        }
        response = self.client.post(
            reverse('create_test-list'),
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
            "question_answer": {
                "13": 7,
                "14": 10
            }
        }

        response = self.client.post(
            reverse('give_answer-list'),
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import override_settings
from django.utils import timezone

from rest_framework.test import APITestCase

from drf_secure_token.models import Token


@override_settings(REMOVE_TOKENS_THROUGH_CELERY=True)
class TaskTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(username='test-user')

    def test_task(self):
        from drf_secure_token.tasks import delete_old_tokens

        live_token = Token.objects.create(user=self.user)
        dead_token = Token.objects.create(user=self.user)
        Token.objects.filter(id=live_token.id).update(dead_in=timezone.now() + timedelta(seconds=5))
        Token.objects.filter(id=dead_token.id).update(dead_in=timezone.now() - timedelta(seconds=5))

        delete_old_tokens()

        self.assertTrue(Token.objects.filter(id=live_token.id).exists())
        self.assertFalse(Token.objects.filter(id=dead_token.id).exists())

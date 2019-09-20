from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework.test import APITestCase

from drf_secure_token.checkers import ActiveUserChecker, DeadTokenChecker, ExpireTokenChecker
from drf_secure_token.models import Token


class CheckersTestCase(APITestCase):
    def test_active_user_checker(self):
        user = get_user_model().objects.create(username='test_user')
        token = Token.objects.create(user=user)

        inactive_user = get_user_model().objects.create(username='inactive_user', is_active=False)
        inactive_token = Token.objects.create(user=inactive_user)

        checker = ActiveUserChecker()

        self.assertTrue(checker.check(token))
        self.assertFalse(checker.check(inactive_token))

    def test_expire_token_checker(self):
        user = get_user_model().objects.create(username='test_user')
        valid_token = Token.objects.create(user=user)
        valid_token.expire_in = timezone.now() + timedelta(seconds=5)

        invalid_token = Token.objects.create(user=user)
        invalid_token.expire_in = timezone.now() - timedelta(seconds=5)

        checker = ExpireTokenChecker()

        self.assertTrue(checker.check(valid_token))
        self.assertFalse(checker.check(invalid_token))
        self.assertFalse(Token.objects.filter(id=invalid_token.id).exists())

    def test_dead_token_checker(self):
        user = get_user_model().objects.create(username='test_user')
        valid_token = Token.objects.create(user=user)
        valid_token.dead_in = timezone.now() + timedelta(seconds=5)

        invalid_token = Token.objects.create(user=user)
        invalid_token.dead_in = timezone.now() - timedelta(seconds=5)

        checker = DeadTokenChecker()

        self.assertTrue(checker.check(valid_token))
        self.assertFalse(checker.check(invalid_token))
        self.assertFalse(Token.objects.filter(id=invalid_token.id).exists())

from datetime import timedelta

from django.contrib.auth.models import User
from mock import patch
from rest_framework import exceptions
from rest_framework.test import APITestCase

from drf_secure_token.models import Token


class ModelsTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user')
        cls.token = Token.objects.create(user=cls.user)

    def test_token_string_representation(self):
        self.assertEqual(str(self.token), self.token.key)

    def test_expire_in(self):
        with self.settings(TOKEN_AGE=60):
            token = Token.objects.create(user=self.user)
            self.assertAlmostEqual(token.expire_in, token.created + timedelta(seconds=60),
                                   delta=timedelta(seconds=1))

    def test_dead_in(self):
        with self.settings(MUTABLE_PERIOD=60):
            token = Token.objects.create(user=self.user)
            self.assertAlmostEqual(token.dead_in, token.expire_in + timedelta(seconds=60),
                                   delta=timedelta(seconds=1))

    @patch('drf_secure_token.checkers.ActiveUserChecker.check')
    @patch('drf_secure_token.checkers.DeadTokenChecker.check')
    def test_checkers(self, *args):
        self.token.check_token()

        for checker in args:
            checker.assert_called_with(self.token)

    @patch('drf_secure_token.checkers.ActiveUserChecker.check', return_value=False)
    def test_fail_checkers(self, mock_check):
        with self.assertRaises(exceptions.AuthenticationFailed):
            self.token.check_token()

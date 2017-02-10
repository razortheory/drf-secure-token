from datetime import timedelta

from django.contrib.auth.models import User
from mock import patch
from rest_framework import exceptions
from rest_framework.test import APITestCase

from drf_secure_token.models import Token
from .models import BaseTokenTestModel, ExpiredTokenTestModel


class ModelsTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user')
        cls.base_token = BaseTokenTestModel.objects.create(user=cls.user)

    def test_token_string_representation(self):
        self.assertEqual(str(self.base_token), self.base_token.key)

    def test_expire_in(self):
        with self.settings(TOKEN_AGE=60):
            expired_token = ExpiredTokenTestModel.objects.create(user=self.user)
            dying_token = Token.objects.create(user=self.user)
            self.assertAlmostEqual(expired_token.expire_in, expired_token.created + timedelta(seconds=60),
                                   delta=timedelta(seconds=1))
            self.assertAlmostEqual(dying_token.expire_in, dying_token.created + timedelta(seconds=60),
                                   delta=timedelta(seconds=1))

    def test_dead_in(self):
        with self.settings(MUTABLE_PERIOD=60):
            dying_token = Token.objects.create(user=self.user)
            self.assertAlmostEqual(dying_token.dead_in, dying_token.expire_in + timedelta(seconds=60),
                                   delta=timedelta(seconds=1))

    @patch('drf_secure_token.checkers.ActiveUserChecker.check')
    @patch('drf_secure_token.checkers.DeadTokenChecker.check')
    def test_checkers(self, *args):
        with self.settings(TOKEN_CHECKERS=['drf_secure_token.checkers.ActiveUserChecker',
                                           'drf_secure_token.checkers.DeadTokenChecker']):
            self.base_token.check_token()

            for checker in args:
                checker.assert_called_with(self.base_token)

    @patch('drf_secure_token.checkers.ActiveUserChecker.check', return_value=False)
    def test_fail_checkers(self, mock_check):
        with self.settings(TOKEN_CHECKERS=['drf_secure_token.checkers.ActiveUserChecker']):
            with self.assertRaises(exceptions.AuthenticationFailed):
                self.base_token.check_token()

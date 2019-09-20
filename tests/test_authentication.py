from django.contrib.auth import get_user_model

from rest_framework import exceptions
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, APITestCase

from mock import patch

from drf_secure_token.authentication import SecureTokenAuthentication
from drf_secure_token.models import Token


class AuthenticationTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(username='test_user')
        cls.request_factory = APIRequestFactory()

    @patch('drf_secure_token.models.Token.check_token')
    def test_calling_checkers(self, mock_check_token):
        token = Token.objects.create(user=self.user)
        request = Request(
            request=self.request_factory.get('/', HTTP_AUTHORIZATION='Token {0}'.format(token)),
            authenticators=[SecureTokenAuthentication()],
        )

        self.assertEqual(request.auth, token)
        self.assertEqual(request.user, self.user)
        self.assertTrue(mock_check_token.called)

    def test_invalid_token(self):
        request = Request(
            request=self.request_factory.get('/', HTTP_AUTHORIZATION='Token INVALID-TOKEN'),
            authenticators=[SecureTokenAuthentication()],
        )

        with self.assertRaises(exceptions.AuthenticationFailed):
            request._authenticate()

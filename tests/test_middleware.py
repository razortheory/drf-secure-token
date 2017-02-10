from datetime import timedelta

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import override_settings
from django.utils import timezone
from rest_framework.request import Request
from rest_framework.test import APITestCase, APIRequestFactory

from drf_secure_token.authentication import SecureTokenAuthentication
from drf_secure_token.middleware import UpdateTokenMiddleware
from drf_secure_token.models import Token


@override_settings(UPDATE_TOKEN=True, TOKEN_CHECKERS=[])
class MiddlewareTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test_user')
        cls.request_factory = APIRequestFactory()

    def test_token_updating(self):
        token = Token.objects.create(user=self.user)
        now = timezone.now()
        Token.objects.update(expire_in=now-timedelta(seconds=5), dead_in=now+timedelta(seconds=5))

        request = Request(request=self.request_factory.get('/', HTTP_AUTHORIZATION='Token %s' % token),
                          authenticators=[SecureTokenAuthentication()])
        request._authenticate()
        response = HttpResponse()

        middleware = UpdateTokenMiddleware()
        response = middleware.process_response(request._request, response)

        new_token = response.get('X-Token', None)
        self.assertIsNotNone(new_token)

        new_token = Token.objects.get(key=new_token)
        self.assertEqual(new_token.user, self.user)

        old_token = Token.objects.get(id=token.id)
        self.assertTrue(old_token.marked_for_delete)

    def test_ignoring_marked_for_delete_tokens(self):
        token = Token.objects.create(user=self.user)
        now = timezone.now()
        Token.objects.update(expire_in=now-timedelta(seconds=5), dead_in=now+timedelta(seconds=5), marked_for_delete=True)

        request = Request(request=self.request_factory.get('/', HTTP_AUTHORIZATION='Token %s' % token),
                          authenticators=[SecureTokenAuthentication()])
        request._authenticate()
        response = HttpResponse()

        middleware = UpdateTokenMiddleware()
        response = middleware.process_response(request._request, response)

        new_token = response.get('X-Token', None)
        self.assertIsNone(new_token)

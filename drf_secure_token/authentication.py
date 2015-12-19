from rest_framework.authentication import BaseAuthentication, get_authorization_header
from drf_secure_token.models import Token
from rest_framework import exceptions

from django.utils.translation import ugettext_lazy as _


class SecureTokenAuthentication(BaseAuthentication):
    model = Token

    # def authenticate(self, request):
    #     auth = get_authorization_header(request).split()
    #
    #     if not auth or auth[0].lower() != b'token':
    #         return None
    #
    #     if len(auth) == 1:
    #         msg = _('Invalid token header. No credentials provided.')
    #         raise exceptions.AuthenticationFailed(msg)
    #     elif len(auth) > 2:
    #         msg = _('Invalid token header. Token string should not contain spaces.')
    #         raise exceptions.AuthenticationFailed(msg)
    #
    #     try:
    #         token = auth[1].decode()
    #     except UnicodeError:
    #         msg = _('Invalid token header. Token string should not contain invalid characters.')
    #         raise exceptions.AuthenticationFailed(msg)
    #
    #     return self.authenticate_credentials(request, token)
    #
    # def authenticate_credentials(self, request, key):
    #     try:
    #         token = self.model.objects.select_related('user').get(key=key)
    #     except self.model.DoesNotExist:
    #         raise exceptions.AuthenticationFailed(_('Invalid token.'))
    #
    #     if not token.user.is_active:
    #         raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
    #     request.META['X-Token'] = token.user.token
    #     user = token.user
    #     token.delete()
    #     return (user, None)
    #
    # def authenticate_header(self, request):
    #     return 'Token'
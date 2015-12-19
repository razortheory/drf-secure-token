from rest_framework.authentication import TokenAuthentication
from drf_secure_token.models import Token


class SecureTokenAuthentication(TokenAuthentication):
    model = Token
from django.http import HttpResponse
from drf_secure_token.models import Token


class UpdateTokenMiddleware(object):
    def process_response(self, request, response):
        auth_token = request.META.get('HTTP_AUTHORIZATION', ' ').split(' ')
        if request.user.is_authenticated() and auth_token[0].lower() == 'token':
            token = Token.objects.filter(key=auth_token[1]).first()
            if token:
                response['X-Token'] = token.update_key()
        return response


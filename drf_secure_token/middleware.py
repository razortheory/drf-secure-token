from django.http import HttpResponse
from drf_secure_token.models import Token


class UpdateTokenMiddleware(object):
    def process_response(self, request, response):
        auth_token = request.META.get('HTTP_AUTHORIZATION', ' ').split(' ')
        if request.user.is_authenticated() and auth_token[0].lower() == 'token':
            tokens = Token.objects.filter(key=auth_token[1])
            if tokens.count():
                new_token = Token.generate_key()
                tokens.update(key=new_token)
                response['X-Token'] = new_token
        return response


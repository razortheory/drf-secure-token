from drf_secure_token.models import Token


class UpdateTokenMiddleware(object):
    def process_response(self, request, response):
        auth_token = request.META.get('HTTP_AUTHORIZATION', ' ').split(' ')
        if hasattr(request, 'user') and request.user.is_authenticated() and auth_token[0].lower() == 'token':
            token = Token.objects.filter(key=auth_token[1])
            if token:
                new_token = Token.generate_key()
                token.update(key=new_token)
                response['X-Token'] = new_token
        return response


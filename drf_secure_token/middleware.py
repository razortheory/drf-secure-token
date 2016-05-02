from django.conf import settings
from django.utils import timezone

from drf_secure_token.models import Token

UPDATE_TOKEN = getattr(settings, 'UPDATE_TOKEN', True)


class UpdateTokenMiddleware(object):
    def process_response(self, request, response):
        auth_token = request.META.get('HTTP_AUTHORIZATION', ' ').split(' ')
        if UPDATE_TOKEN and hasattr(request, 'user') and request.user.is_authenticated() and auth_token[0].lower() == 'token':
            token = Token.objects.filter(key=auth_token[1]).first()

            now = timezone.now()

            if token and not token.marked_for_delete and token.expire_in < now < token.dead_in:
                token.marked_for_delete = True
                token.save()

                new_token = Token.objects.create(user=request.user)

                response['X-Token'] = new_token.key
        return response


from django.utils import timezone

from drf_secure_token.models import Token
from drf_secure_token.settings import UPDATE_TOKEN


class UpdateTokenMiddleware(object):
    def process_response(self, request, response):
        token = getattr(request, 'auth', None)
        if not isinstance(token, Token):
            return response

        if UPDATE_TOKEN:
            now = timezone.now()

            if not token.marked_for_delete and token.expire_in < now < token.dead_in:
                token.marked_for_delete = True
                token.save()

                new_token = Token.objects.create(user=request.user)

                response['X-Token'] = new_token.key

        return response


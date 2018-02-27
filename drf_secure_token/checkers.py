from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from rest_framework.settings import perform_import

from drf_secure_token.settings import settings as token_settings


class BaseChecker(object):
    error_message = u''

    def check(self, token):
        raise NotImplementedError('`check` method must be implemented.')


class ActiveUserChecker(BaseChecker):
    error_message = _('User inactive or deleted.')

    def check(self, token):
        return token.user.is_active


class ExpireTokenChecker(BaseChecker):
    error_message = _('Token has expired.')

    def check(self, token):
        valid = token.expire_in > timezone.now()
        if not valid:
            token.delete()
        return valid


class DeadTokenChecker(ExpireTokenChecker):
    def check(self, token):
        valid = token.dead_in > timezone.now()
        if not valid:
            token.delete()
        return valid


def init_checkers():
    checker_classes = perform_import(token_settings.TOKEN_CHECKERS, 'TOKEN_CHECKERS')
    return list(map(lambda klass: klass(), checker_classes))


checkers = init_checkers()

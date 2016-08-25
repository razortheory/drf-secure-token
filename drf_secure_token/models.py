from django.utils.translation import ugettext_lazy as _

from drf_secure_token.abstract_models import BaseToken, DyingTokenMixin


class Token(DyingTokenMixin, BaseToken):
    class Meta:
        verbose_name = _('Token')
        verbose_name_plural = _('Tokens')

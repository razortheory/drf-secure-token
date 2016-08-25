from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DRFSecureTokenConfig(AppConfig):
    name = 'drf_secure_token'
    verbose_name = _('DRF Secure Token')

from drf_secure_token.abstract_models import BaseToken, ExpiredTokenMixin


class BaseTokenTestModel(BaseToken):
    pass


class ExpiredTokenTestModel(ExpiredTokenMixin, BaseToken):
    pass

import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class SymbolValidator(object):
    symbols = "!#$%&()*+,-./:;<=>?@^_`{|}~"

    def validate(self, password, user=None):
        if not re.findall(f"[{self.symbols}]", password):
            raise ValidationError(
                _(f"The password must contain at least 1 symbol: {self.symbols}"),
                code="password_no_symbol",
            )

    def get_help_text(self):
        return _(f"Your password must contain at least 1 symbol: {self.symbols}")

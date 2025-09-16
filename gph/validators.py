from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class AsciiPasswordValidator:
    def validate(self, password, user=None):
        if not password.isascii():
            raise ValidationError(
                _("비밀번호는 영문, 숫자, 기호만 사용할 수 있습니다. (ex. Puzz!eHunt1)"),
                code='password_not_ascii',
            )

    def get_help_text(self):
        return _(
            "비밀번호는 영문, 숫자, 기호만 사용할 수 있습니다. (ex. Puzz!eHunt1)"
        )

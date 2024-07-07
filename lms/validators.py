from rest_framework.serializers import ValidationError


class VideoLinkValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp = dict(value).get(self.field)
        if tmp:
            if not tmp.startswith("https://youtube.com/"):
                raise ValidationError(
                    "Некорректная ссылка. Разрешены только ссылки на Youtube."
                )

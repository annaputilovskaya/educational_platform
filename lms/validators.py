from rest_framework.serializers import ValidationError


class VideoLinkValidator:
    """
    Валидатор ссылки на видео.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        """
        Проверяет, что ссылка ведет к видео на Youtube.
        """
        tmp = dict(value).get(self.field)
        if tmp:
            if not tmp.startswith("https://youtube.com/"):
                raise ValidationError(
                    "Некорректная ссылка. Разрешены только ссылки на Youtube."
                )

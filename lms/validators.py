import re

from rest_framework.serializers import ValidationError


class VideoLinkValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile(r'https:\/\/www.youtube.com')
        tmp = dict(value).get(self.field)
        if not bool(reg.match(tmp)):
            raise ValidationError("Некорректная ссылка. Разрешены только ссылки на Youtube.")

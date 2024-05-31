import re

from rest_framework import serializers
from rest_framework.serializers import ValidationError


class TitleValodator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile('^[a-zA-Z0-9\.\-\ ]+s')
        tmp_val = value.get(self.field)
        if not bool(reg.match(tmp_val)):
            raise ValidationError('Title is not ok')


class YouTubeLinkValidator:
    def __init__(self, field):
        self.field = field
    def __call__(self, value):
        youtube_pattern = re.compile(r'^https?://(?:www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]+')
        if not youtube_pattern.match(value['video_link']):
            raise ValidationError("Вы используете ссылку на сторонние образовательные платформы, a можно только с YouTube.com")
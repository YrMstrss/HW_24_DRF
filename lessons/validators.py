from rest_framework.exceptions import ValidationError


class VideoLinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_value = dict(value).get(self.field)
        if not ('youtube.com' in tmp_value or '127.0.0.1:8000' in tmp_value or 'localhost:8000' in tmp_value):
            raise ValidationError('Ссылка на сторонний ресурс')

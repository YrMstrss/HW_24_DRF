from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=50, verbose_name='название курса')
    preview = models.ImageField(upload_to='courses/', verbose_name='превью курса', **NULLABLE)
    description = models.TextField(verbose_name='описание курса')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

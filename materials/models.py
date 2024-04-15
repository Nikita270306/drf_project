from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200)
    preview = models.ImageField(upload_to='previews/')
    description = models.TextField()

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    preview = models.ImageField(upload_to='lesson_previews/')
    video_link = models.URLField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'




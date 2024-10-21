from django.db import models
NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    """Класс модели блога"""
    title = models.CharField(max_length=150, verbose_name='заголовок')
    slug = models.CharField(max_length=150, verbose_name='slug', **NULLABLE)
    content = models.TextField(verbose_name='контент')
    preview = models.ImageField(upload_to='blog/image', verbose_name='Изображение', **NULLABLE)
    created_at = models.DateField(auto_now_add=True, verbose_name='дата создания', **NULLABLE)
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
        permissions = [
            ('can_add_blog', 'Can add blog'),
            ('can_view_blog', 'Can view blog'),
            ('can_change_blog', 'Can change blog'),
            ('can_delete_blog', 'Can delete blog'),
        ]





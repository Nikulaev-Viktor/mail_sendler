# Generated by Django 4.2 on 2024-10-15 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Blog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=150, verbose_name="заголовок")),
                (
                    "slug",
                    models.CharField(
                        blank=True, max_length=150, null=True, verbose_name="slug"
                    ),
                ),
                ("content", models.TextField(verbose_name="контент")),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="blog/image",
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "created_at",
                    models.DateField(
                        auto_now_add=True, null=True, verbose_name="дата создания"
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(default=True, verbose_name="опубликовано"),
                ),
                (
                    "views_count",
                    models.IntegerField(
                        default=0, verbose_name="количество просмотров"
                    ),
                ),
            ],
            options={
                "verbose_name": "блог",
                "verbose_name_plural": "блоги",
            },
        ),
    ]

# Generated by Django 2.2.16 on 2022-05-22 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_auto_20220522_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.Review', verbose_name='Дата публикации'),
        ),
    ]

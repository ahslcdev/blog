# Generated by Django 4.2 on 2024-03-08 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id_comentarios',
            field=models.ManyToManyField(blank=True, to='core.comment', verbose_name='Comentários'),
        ),
    ]

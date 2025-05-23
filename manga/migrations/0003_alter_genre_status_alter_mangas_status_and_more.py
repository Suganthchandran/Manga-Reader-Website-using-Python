# Generated by Django 5.0.6 on 2024-06-02 21:14

import django.db.models.deletion
import manga.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0002_remove_genre_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='status',
            field=models.BooleanField(default=False, help_text='0-show, 1-Hidden'),
        ),
        migrations.AlterField(
            model_name='mangas',
            name='status',
            field=models.BooleanField(default=False, help_text='0-show, 1-Hidden'),
        ),
        migrations.AlterField(
            model_name='mangas',
            name='trending',
            field=models.BooleanField(default=False, help_text='0-default, 1-trending'),
        ),
        migrations.AlterField(
            model_name='mangas',
            name='work_status',
            field=models.BooleanField(default=False, help_text='0-ongoing, 1-Completed'),
        ),
        migrations.CreateModel(
            name='MangaFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=manga.models.getFileName)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('manga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manga.mangas')),
            ],
        ),
        migrations.AddField(
            model_name='mangas',
            name='files',
            field=models.ManyToManyField(related_name='mangas', to='manga.mangafile'),
        ),
    ]

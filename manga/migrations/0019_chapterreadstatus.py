# Generated by Django 5.0.6 on 2024-11-14 17:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0018_rename_anime_adaption_mangas_adaption'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChapterReadStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False)),
                ('read_at', models.DateTimeField(blank=True, null=True)),
                ('library', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manga.library')),
                ('pdf_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manga.pdffile')),
            ],
        ),
    ]
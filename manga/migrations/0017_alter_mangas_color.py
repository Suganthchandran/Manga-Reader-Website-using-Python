# Generated by Django 5.0.6 on 2024-11-14 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0016_remove_mangas_adaption_mangas_anime_adaption'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mangas',
            name='color',
            field=models.CharField(choices=[('black_and_white', 'Black and White'), ('color', 'Color')], default='color', max_length=15),
        ),
    ]
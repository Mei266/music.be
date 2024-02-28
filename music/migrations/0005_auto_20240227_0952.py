# Generated by Django 3.2 on 2024-02-27 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_auto_20240220_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='duration',
            field=models.CharField(default='0:00', max_length=10),
        ),
        migrations.AlterField(
            model_name='music',
            name='artist',
            field=models.ManyToManyField(related_name='artist_item', through='music.ArtistItem', to='music.Artist'),
        ),
    ]

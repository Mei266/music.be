# Generated by Django 3.2 on 2024-02-27 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0005_auto_20240227_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='duration',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]

# Generated by Django 3.2 on 2024-02-27 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0008_heart'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='heart',
            options={'ordering': ['created_at'], 'verbose_name': 'Heart'},
        ),
    ]

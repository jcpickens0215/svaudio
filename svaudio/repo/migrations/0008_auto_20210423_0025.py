# Generated by Django 3.1.8 on 2021-04-23 00:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0007_auto_20210419_1538'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='file',
            options={'ordering': ['-cached_at']},
        ),
    ]
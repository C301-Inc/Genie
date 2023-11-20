# Generated by Django 4.1.7 on 2023-11-20 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_inbox_secret_key_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialaccount',
            name='did_connect_lastfm',
            field=models.BooleanField(default=False, help_text='did connect last.fm', verbose_name='did connect last.fm'),
        ),
        migrations.AddField(
            model_name='socialaccount',
            name='lastfm_id',
            field=models.CharField(blank=True, help_text='last.fm id', max_length=50, null=True, unique=True, verbose_name='last.fm id'),
        ),
    ]

# Generated by Django 4.1.7 on 2023-11-24 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blockchain', '0004_alter_cointransactionhistory_server_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='coin',
            name='decimal',
            field=models.IntegerField(default=0, verbose_name='decimal'),
            preserve_default=False,
        ),
    ]

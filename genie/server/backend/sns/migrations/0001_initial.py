# Generated by Django 4.1.7 on 2023-10-15 18:53

import backend.utils.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created at model')),
                ('created_by', models.IntegerField(blank=True, help_text='user creates model', null=True, verbose_name='user creates model')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at model')),
                ('updated_by', models.IntegerField(blank=True, help_text='user updates model', null=True, verbose_name='user updates model')),
                ('is_deleted', models.BooleanField(default=False, help_text='just flag, not delete data actually', verbose_name='Whether model is deleted')),
                ('name', models.CharField(help_text='SNS server name (ex. ATIV, NOIS, ...)', max_length=50, verbose_name='SNS server name')),
            ],
            options={
                'verbose_name': 'Server',
                'verbose_name_plural': 'Server',
            },
            bases=(models.Model, backend.utils.models.PrintableMixin),
        ),
        migrations.CreateModel(
            name='SNS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created at model')),
                ('created_by', models.IntegerField(blank=True, help_text='user creates model', null=True, verbose_name='user creates model')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at model')),
                ('updated_by', models.IntegerField(blank=True, help_text='user updates model', null=True, verbose_name='user updates model')),
                ('is_deleted', models.BooleanField(default=False, help_text='just flag, not delete data actually', verbose_name='Whether model is deleted')),
                ('name', models.CharField(help_text='SNS name (ex. Discord, Twitter ...)', max_length=50, unique=True, verbose_name='SNS name')),
            ],
            options={
                'verbose_name': 'SNS',
                'verbose_name_plural': 'SNS',
            },
            bases=(models.Model, backend.utils.models.PrintableMixin),
        ),
        migrations.CreateModel(
            name='SNSConnectionInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created at model')),
                ('created_by', models.IntegerField(blank=True, help_text='user creates model', null=True, verbose_name='user creates model')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at model')),
                ('updated_by', models.IntegerField(blank=True, help_text='user updates model', null=True, verbose_name='user updates model')),
                ('is_deleted', models.BooleanField(default=False, help_text='just flag, not delete data actually', verbose_name='Whether model is deleted')),
                ('handle', models.CharField(help_text='SNS handle', max_length=50, verbose_name='SNS handle')),
                ('discriminator', models.CharField(help_text='SNS discriminator', max_length=100, verbose_name='SNS discriminator')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sns_info', to='accounts.socialaccount')),
                ('sns', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='users_info', to='sns.sns')),
            ],
            options={
                'verbose_name': 'SNS-SocialAccount info',
                'verbose_name_plural': 'SNS-SocialAccount info',
            },
            bases=(models.Model, backend.utils.models.PrintableMixin),
        ),
        migrations.CreateModel(
            name='ServerHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created at model')),
                ('created_by', models.IntegerField(blank=True, help_text='user creates model', null=True, verbose_name='user creates model')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at model')),
                ('updated_by', models.IntegerField(blank=True, help_text='user updates model', null=True, verbose_name='user updates model')),
                ('is_deleted', models.BooleanField(default=False, help_text='just flag, not delete data actually', verbose_name='Whether model is deleted')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Date stored history')),
                ('member_count', models.IntegerField(null=True, verbose_name='# of server members')),
                ('daily_chat_count', models.IntegerField(null=True, verbose_name='# of chats in server')),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='histories', to='sns.server')),
            ],
            options={
                'verbose_name': 'Server History',
                'verbose_name_plural': 'Server History',
            },
            bases=(models.Model, backend.utils.models.PrintableMixin),
        ),
        migrations.AddField(
            model_name='server',
            name='sns',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='servers', to='sns.sns'),
        ),
        migrations.AddConstraint(
            model_name='snsconnectioninfo',
            constraint=models.UniqueConstraint(fields=('sns', 'handle', 'discriminator'), name='unique sns handle'),
        ),
        migrations.AddConstraint(
            model_name='server',
            constraint=models.UniqueConstraint(fields=('sns', 'name'), name='unique (sns, server)'),
        ),
    ]

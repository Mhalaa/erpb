# Generated by Django 5.1.7 on 2025-04-06 16:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pams', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='btcashrequest',
            name='archived_reason',
        ),
        migrations.RemoveField(
            model_name='btcashrequest',
            name='items',
        ),
        migrations.RemoveField(
            model_name='btcashrequest',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='btcashrequest',
            name='purpose',
        ),
        migrations.RemoveField(
            model_name='company',
            name='description',
        ),
        migrations.RemoveField(
            model_name='company',
            name='name',
        ),
        migrations.RemoveField(
            model_name='mediaproject',
            name='description',
        ),
        migrations.RemoveField(
            model_name='mediaproject',
            name='name',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='archived_reason',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='items',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='purpose',
        ),
        migrations.RemoveField(
            model_name='transactionlog',
            name='description',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='name',
        ),
        migrations.RemoveField(
            model_name='vendortransaction',
            name='details',
        ),
        migrations.AddField(
            model_name='btcashrequest',
            name='archived_reason_ar',
            field=models.TextField(blank=True, verbose_name='Archived Reason (Arabic)'),
        ),
        migrations.AddField(
            model_name='btcashrequest',
            name='archived_reason_en',
            field=models.TextField(blank=True, verbose_name='Archived Reason (English)'),
        ),
        migrations.AddField(
            model_name='btcashrequest',
            name='currency',
            field=models.CharField(choices=[('USD', 'US Dollar'), ('SAR', 'Saudi Riyal'), ('EGP', 'Egyptian Pound'), ('EUR', 'Euro')], default='USD', max_length=3),
        ),
        migrations.AddField(
            model_name='btcashrequest',
            name='items_ar',
            field=models.TextField(default='', verbose_name='Items (Arabic)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='btcashrequest',
            name='items_en',
            field=models.TextField(default='', verbose_name='Items (English)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='btcashrequest',
            name='notes_ar',
            field=models.TextField(blank=True, verbose_name='Notes (Arabic)'),
        ),
        migrations.AddField(
            model_name='btcashrequest',
            name='notes_en',
            field=models.TextField(blank=True, verbose_name='Notes (English)'),
        ),
        migrations.AddField(
            model_name='btcashrequest',
            name='purpose_ar',
            field=models.CharField(default='', max_length=100, verbose_name='Purpose (Arabic)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='btcashrequest',
            name='purpose_en',
            field=models.CharField(default='', max_length=100, verbose_name='Purpose (English)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='description_ar',
            field=models.TextField(blank=True, verbose_name='Description (Arabic)'),
        ),
        migrations.AddField(
            model_name='company',
            name='description_en',
            field=models.TextField(blank=True, verbose_name='Description (English)'),
        ),
        migrations.AddField(
            model_name='company',
            name='name_ar',
            field=models.CharField(default='', max_length=100, unique=True, verbose_name='Name (Arabic)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='name_en',
            field=models.CharField(default='', max_length=100, unique=True, verbose_name='Name (English)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mediaproject',
            name='currency',
            field=models.CharField(choices=[('USD', 'US Dollar'), ('SAR', 'Saudi Riyal'), ('EGP', 'Egyptian Pound'), ('EUR', 'Euro')], default='USD', max_length=3),
        ),
        migrations.AddField(
            model_name='mediaproject',
            name='description_ar',
            field=models.TextField(blank=True, verbose_name='Description (Arabic)'),
        ),
        migrations.AddField(
            model_name='mediaproject',
            name='description_en',
            field=models.TextField(blank=True, verbose_name='Description (English)'),
        ),
        migrations.AddField(
            model_name='mediaproject',
            name='name_ar',
            field=models.CharField(default='', max_length=100, verbose_name='Name (Arabic)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mediaproject',
            name='name_en',
            field=models.CharField(default='', max_length=100, verbose_name='Name (English)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='archived_reason_ar',
            field=models.TextField(blank=True, verbose_name='Archived Reason (Arabic)'),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='archived_reason_en',
            field=models.TextField(blank=True, verbose_name='Archived Reason (English)'),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='currency',
            field=models.CharField(choices=[('USD', 'US Dollar'), ('SAR', 'Saudi Riyal'), ('EGP', 'Egyptian Pound'), ('EUR', 'Euro')], default='USD', max_length=3),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='items_ar',
            field=models.TextField(default='', verbose_name='Items (Arabic)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='items_en',
            field=models.TextField(default='', verbose_name='Items (English)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='notes_ar',
            field=models.TextField(blank=True, verbose_name='Notes (Arabic)'),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='notes_en',
            field=models.TextField(blank=True, verbose_name='Notes (English)'),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='purpose_ar',
            field=models.CharField(default='', max_length=100, verbose_name='Purpose (Arabic)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='purpose_en',
            field=models.CharField(default='', max_length=100, verbose_name='Purpose (English)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionlog',
            name='description_ar',
            field=models.TextField(default='', verbose_name='Description (Arabic)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionlog',
            name='description_en',
            field=models.TextField(default='', verbose_name='Description (English)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='preferred_currency',
            field=models.CharField(choices=[('USD', 'US Dollar'), ('SAR', 'Saudi Riyal'), ('EGP', 'Egyptian Pound'), ('EUR', 'Euro')], default='USD', max_length=3),
        ),
        migrations.AddField(
            model_name='vendor',
            name='name_ar',
            field=models.CharField(default='', max_length=100, verbose_name='Name (Arabic)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vendor',
            name='name_en',
            field=models.CharField(default='', max_length=100, verbose_name='Name (English)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vendortransaction',
            name='currency',
            field=models.CharField(choices=[('USD', 'US Dollar'), ('SAR', 'Saudi Riyal'), ('EGP', 'Egyptian Pound'), ('EUR', 'Euro')], default='USD', max_length=3),
        ),
        migrations.AddField(
            model_name='vendortransaction',
            name='details_ar',
            field=models.TextField(blank=True, verbose_name='Details (Arabic)'),
        ),
        migrations.AddField(
            model_name='vendortransaction',
            name='details_en',
            field=models.TextField(blank=True, verbose_name='Details (English)'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='contact_info',
            field=models.TextField(blank=True, verbose_name='Contact Info'),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_en', models.CharField(max_length=100, verbose_name='Title (English)')),
                ('title_ar', models.CharField(max_length=100, verbose_name='Title (Arabic)')),
                ('message_en', models.TextField(verbose_name='Message (English)')),
                ('message_ar', models.TextField(verbose_name='Message (Arabic)')),
                ('type', models.CharField(choices=[('info', 'Info'), ('warning', 'Warning'), ('success', 'Success'), ('error', 'Error')], default='info', max_length=20)),
                ('is_read', models.BooleanField(default=False)),
                ('related_object', models.CharField(blank=True, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
            },
        ),
    ]

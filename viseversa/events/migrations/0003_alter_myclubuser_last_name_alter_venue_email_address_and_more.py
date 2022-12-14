# Generated by Django 4.1 on 2022-08-28 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_alter_event_venue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myclubuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='venue',
            name='email_address',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Email Address'),
        ),
        migrations.AlterField(
            model_name='venue',
            name='web',
            field=models.URLField(blank=True, verbose_name='Website Address'),
        ),
        migrations.AlterField(
            model_name='venue',
            name='zip_code',
            field=models.CharField(blank=True, max_length=15, verbose_name='Zip Code'),
        ),
    ]

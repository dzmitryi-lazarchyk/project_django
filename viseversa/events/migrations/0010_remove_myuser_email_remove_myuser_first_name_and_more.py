# Generated by Django 4.1 on 2022-09-20 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_myuser_delete_myclubuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='email',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='last_name',
        ),
        migrations.AddField(
            model_name='myuser',
            name='ava',
            field=models.ImageField(blank=True, null=True, upload_to='images_avas/'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='venue',
            name='venue_image',
            field=models.ImageField(blank=True, null=True, upload_to='images_venues/'),
        ),
    ]

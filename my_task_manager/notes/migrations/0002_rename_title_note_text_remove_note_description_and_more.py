# Generated by Django 5.1.6 on 2025-02-19 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='title',
            new_name='text',
        ),
        migrations.RemoveField(
            model_name='note',
            name='description',
        ),
        migrations.RemoveField(
            model_name='note',
            name='is_completed',
        ),
    ]

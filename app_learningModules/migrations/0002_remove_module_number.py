# Generated by Django 5.0 on 2024-01-14 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_learningModules', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='number',
        ),
    ]
# Generated by Django 5.0.1 on 2024-02-06 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faunatrack', '0005_alter_observation_date_observation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation',
            name='date_observation',
            field=models.DateTimeField(),
        ),
    ]

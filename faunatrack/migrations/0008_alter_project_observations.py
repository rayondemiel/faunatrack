# Generated by Django 5.0.1 on 2024-02-07 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faunatrack', '0007_project_slug_alter_observation_date_observation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='observations',
            field=models.ManyToManyField(related_name='projets', to='faunatrack.observation'),
        ),
    ]

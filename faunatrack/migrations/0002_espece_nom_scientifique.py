# Generated by Django 5.0.1 on 2024-02-05 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faunatrack', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='espece',
            name='nom_scientifique',
            field=models.CharField(max_length=250, null=True),
        ),
    ]

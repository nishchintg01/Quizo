# Generated by Django 3.0.5 on 2020-12-02 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levels', '0006_quiz_attempted'),
    ]

    operations = [
        migrations.AddField(
            model_name='answers',
            name='time_taken',
            field=models.IntegerField(default=0),
        ),
    ]

# Generated by Django 3.0.5 on 2020-12-02 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levels', '0008_auto_20201203_0000'),
    ]

    operations = [
        migrations.AddField(
            model_name='answers',
            name='explaination',
            field=models.TextField(default='sad'),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.1.5 on 2021-01-27 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('holiday', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='status',
            field=models.CharField(default='panding', max_length=225),
        ),
    ]

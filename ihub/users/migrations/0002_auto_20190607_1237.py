# Generated by Django 2.2.1 on 2019-06-07 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='matric',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-16 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitors', '0005_alter_session_session_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='session_end',
            field=models.DateTimeField(null=True),
        ),
    ]

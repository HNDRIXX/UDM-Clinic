# Generated by Django 4.2.1 on 2023-06-26 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_illness'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='empPhoneNum',
            field=models.IntegerField(default=0, max_length=11),
        ),
    ]

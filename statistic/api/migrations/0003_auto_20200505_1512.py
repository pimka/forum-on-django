# Generated by Django 3.0.3 on 2020-05-05 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200505_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statisicmodel',
            name='operation',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='statisicmodel',
            name='user_uuid',
            field=models.UUIDField(null=True),
        ),
    ]

# Generated by Django 5.1.1 on 2024-09-24 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_alter_service_description_servicesimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='customer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='service',
            name='quality',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='service',
            name='supports',
            field=models.BooleanField(default=False),
        ),
    ]

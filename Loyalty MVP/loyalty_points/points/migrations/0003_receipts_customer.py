# Generated by Django 5.0.3 on 2024-03-18 15:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0002_alter_customuser_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipts',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]

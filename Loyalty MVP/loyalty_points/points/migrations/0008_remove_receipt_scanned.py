# Generated by Django 5.0.3 on 2024-04-01 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0007_receipt_delete_receipts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receipt',
            name='scanned',
        ),
    ]
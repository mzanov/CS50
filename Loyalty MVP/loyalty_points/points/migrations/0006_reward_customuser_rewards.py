# Generated by Django 5.0.3 on 2024-03-19 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0005_alter_customuser_points_history'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reward_name', models.CharField(max_length=100)),
                ('points_requirement', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='rewards',
            field=models.ManyToManyField(to='points.reward'),
        ),
    ]

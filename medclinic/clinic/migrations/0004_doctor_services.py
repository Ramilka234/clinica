# Generated by Django 5.0.6 on 2024-06-06 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0003_news_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='services',
            field=models.ManyToManyField(related_name='doctors', to='clinic.service'),
        ),
    ]
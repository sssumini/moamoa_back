# Generated by Django 4.1.7 on 2023-08-15 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_review_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='rating',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]

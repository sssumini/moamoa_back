# Generated by Django 4.1.7 on 2023-08-13 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_store_boards_remove_store_chat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='price',
            field=models.CharField(max_length=100),
        ),
    ]

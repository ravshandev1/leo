# Generated by Django 4.2 on 2024-09-04 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_remove_store_image_remove_store_link'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserPointImage',
        ),
    ]

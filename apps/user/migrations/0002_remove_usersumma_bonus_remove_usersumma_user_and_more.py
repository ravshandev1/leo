# Generated by Django 4.2 on 2024-10-04 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_bonus_remove_product_bonus_usersumma_bonus_product'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersumma',
            name='bonus',
        ),
        migrations.RemoveField(
            model_name='usersumma',
            name='user',
        ),
        migrations.DeleteModel(
            name='Bonus',
        ),
        migrations.DeleteModel(
            name='UserSumma',
        ),
    ]

# Generated by Django 4.2 on 2024-09-24 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='subcategories/'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='product.subcategory'),
        ),
    ]
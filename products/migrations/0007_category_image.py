# Generated by Django 3.2.10 on 2022-06-30 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_featuredproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
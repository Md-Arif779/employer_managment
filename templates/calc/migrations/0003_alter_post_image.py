# Generated by Django 3.2.5 on 2021-07-30 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0002_post_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='Image',
            field=models.ImageField(upload_to='media/images'),
        ),
    ]

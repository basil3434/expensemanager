# Generated by Django 5.0.6 on 2024-08-13 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_category_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='catimage'),
        ),
    ]
# Generated by Django 5.0.3 on 2024-03-17 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_api', '0004_alter_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='user_id',
            field=models.CharField(max_length=255),
        ),
    ]

# Generated by Django 5.0.3 on 2024-03-17 05:37

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_api', '0002_alter_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
# Generated by Django 4.2.23 on 2025-07-24 04:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="updated",
            field=models.DateTimeField(auto_now=True),
        ),
    ]

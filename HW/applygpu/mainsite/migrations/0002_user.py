# Generated by Django 4.2.11 on 2024-05-14 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainsite", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "studentId",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
                ("email", models.EmailField(max_length=150, unique=True)),
                ("password", models.CharField(max_length=100)),
            ],
        ),
    ]

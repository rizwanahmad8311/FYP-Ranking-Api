# Generated by Django 4.2 on 2023-05-28 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0009_alter_project_reviews_stars"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="website_link",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]

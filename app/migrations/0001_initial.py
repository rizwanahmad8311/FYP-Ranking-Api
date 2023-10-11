# Generated by Django 3.2.9 on 2023-04-08 07:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_title', models.CharField(max_length=200)),
                ('project_description', models.CharField(max_length=200)),
                ('user_batch', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('supervisor_name', models.CharField(max_length=20)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Project_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_category', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Project_Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.FloatField()),
                ('feedback', models.CharField(max_length=250)),
                ('feedback_date', models.DateTimeField()),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projectid', to='app.project')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userid', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project_Images_Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_image', models.ImageField(upload_to='images/')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_id', to='app.project')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='project_category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_category_id', to='app.project_category'),
        ),
        migrations.AddField(
            model_name='project',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_id', to=settings.AUTH_USER_MODEL),
        ),
    ]
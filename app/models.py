from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class User_Activation(models.Model):
    uuid = models.CharField(max_length=250)
    user = models.ForeignKey(User, related_name="user",
                             on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def register(self):
        self.save()


class Project_Category(models.Model):
    project_category = models.CharField(max_length=200)

    def __str__(self):
        return self.project_category


class Project(models.Model):
    user_id = models.ForeignKey(
        User, related_name="user_id", on_delete=models.CASCADE)
    project_category_id = models.ForeignKey(
        Project_Category, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=200)
    project_description = models.CharField(max_length=200)
    user_batch = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    project_image = models.ImageField(upload_to='images/')
    supervisor_name = models.CharField(max_length=20)
    status = models.BooleanField(default=False)
    website_link = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.project_title


class Project_Images_Gallery(models.Model):
    project_id = models.ForeignKey(
        Project, related_name="project_id", on_delete=models.CASCADE)
    project_image = models.ImageField(upload_to='images/')


class Project_Reviews(models.Model):
    user_id = models.ForeignKey(
        User, related_name="userid", on_delete=models.CASCADE)
    project_id = models.ForeignKey(
        Project, related_name="projectid", on_delete=models.CASCADE)
    stars = models.FloatField(null=True,blank=True)
    feedback = models.CharField(max_length=250)
    feedback_date = models.DateTimeField()
    feedback_update_date = models.DateTimeField()

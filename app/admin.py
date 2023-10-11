from django.contrib import admin
from . import models


admin.site.site_header = "FYP RANKING ADMIN"
admin.site.site_title = "FYP RANKING ADMIN PORTAL"
admin.site.index_title = "WELCOME TO FYP RANKING ADMIN PORTAL"


@admin.register(models.User_Activation)
class UserActivationAdmin(admin.ModelAdmin):
    list_display = ['id', 'uuid', 'user', 'active']


@admin.register(models.Project_Category)
class Project_Category_Admin(admin.ModelAdmin):
    list_display = ['id', 'project_category']


@admin.register(models.Project)
class Project_Admin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'project_category_id', 'project_title',
                    'project_description', 'user_batch', 'created_at', 'updated_at', 'project_image','supervisor_name','website_link', 'status']


@admin.register(models.Project_Images_Gallery)
class Project_Images_Gallery_Admin(admin.ModelAdmin):
    list_display = ['id', 'project_id', 'project_image']


@admin.register(models.Project_Reviews)
class Project_Reviews_Admin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'project_id', 'stars',
                    'feedback', 'feedback_date', 'feedback_update_date']

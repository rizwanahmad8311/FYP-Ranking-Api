from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project, Project_Reviews,Project_Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        # extra_kwargs = {'first_name':{'required':True},'last_name':{'required':True},'email':{'required':True},'password': {'write_only': True},}
        extra_kwargs = {
            'first_name': {
                'required': True,
                'error_messages': {
                    "required": "First Name is required",
                }
            },
            'last_name': {
                'required': True,
                'error_messages': {
                    "required": "Last Name is required",
                }
            },
            'email': {
                'required': True,
                'error_messages': {
                    "required": "Email is required",
                }
            },
            'password': {
                'write_only': True,
                'error_messages': {
                    "required": "Password is required",
                }
            },
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'password','username','email']
        extra_kwargs = {'password': {'required': False},'username': {'required': False}, }


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        # fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        fields = ['id', 'project_category_id', 'project_title',
                  'project_description', 'user_batch','project_image','website_link', 'supervisor_name']
        # extra_kwargs = {'created_at': {'read_only': True}, 'updated_at': {'read_only': True}}


class GetProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'user_id', 'project_category_id', 'project_title', 'project_description',
                  'user_batch','project_image','supervisor_name', 'website_link', 'created_at', 'updated_at', 'status']


class ProjectReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project_Reviews
        fields = ['id','feedback']


class GetProjectReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project_Reviews
        fields = ['id', 'user_id', 'project_id',
                  'stars', 'feedback', 'feedback_date','feedback_update_date',]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Project_Category
        fields = ['id', 'project_category']

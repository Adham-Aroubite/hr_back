# ==== core/serializers.py (create this new file) ====
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Company, UserProfile, JobPosting, ResumeData, JobApplication, Interview

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'

class JobPostingSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = JobPosting
        fields = '__all__'

class ResumeDataSerializer(serializers.ModelSerializer):
    candidate = UserSerializer(read_only=True)
    
    class Meta:
        model = ResumeData
        fields = '__all__'

class JobApplicationSerializer(serializers.ModelSerializer):
    job_posting = JobPostingSerializer(read_only=True)
    candidate = UserSerializer(read_only=True)
    resume_data = ResumeDataSerializer(read_only=True)
    
    class Meta:
        model = JobApplication
        fields = '__all__'

class InterviewSerializer(serializers.ModelSerializer):
    application = JobApplicationSerializer(read_only=True)
    interviewer = UserSerializer(read_only=True)
    
    class Meta:
        model = Interview
        fields = '__all__'
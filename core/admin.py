# ==== core/admin.py ====
from django.contrib import admin
from .models import Company, UserProfile, JobPosting, ResumeData, JobApplication, Interview

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'registration_code', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'registration_code']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'company', 'created_at']
    list_filter = ['user_type', 'company', 'created_at']
    search_fields = ['user__username', 'user__email']

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'department', 'status', 'created_at']
    list_filter = ['status', 'company', 'department', 'job_type', 'created_at']
    search_fields = ['title', 'description', 'company__name']
    readonly_fields = ['public_id', 'created_at', 'updated_at']

@admin.register(ResumeData)
class ResumeDataAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'candidate', 'email', 'original_file_name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['full_name', 'email', 'candidate__username']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'job_posting', 'status', 'ai_match_score', 'applied_at']
    list_filter = ['status', 'job_posting__company', 'applied_at']
    search_fields = ['candidate__username', 'job_posting__title']
    readonly_fields = ['applied_at', 'updated_at']

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ['application', 'interviewer', 'interview_type', 'scheduled_time', 'status']
    list_filter = ['status', 'interview_type', 'scheduled_time']
    search_fields = ['application__candidate__username', 'interviewer__username']
    readonly_fields = ['created_at', 'updated_at']
# ==== core/models.py ====
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Company(models.Model):
    name = models.CharField(max_length=200)
    registration_code = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Optional company details
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Companies"
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    USER_TYPES = [
        ('HR', 'HR Member'),
        ('CANDIDATE', 'Candidate'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} ({self.user_type})"

class JobPosting(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('ACTIVE', 'Active'),
        ('PAUSED', 'Paused'),
        ('CLOSED', 'Closed'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    
    # Public link for sharing
    public_id = models.UUIDField(default=uuid.uuid4, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.company.name}"

class ResumeData(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Personal Information
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    
    # Professional Summary
    summary = models.TextField(blank=True, null=True)
    
    # Experience (JSON field for flexibility)
    experience = models.JSONField(default=list)
    skills = models.JSONField(default=list)
    education = models.JSONField(default=list)
    
    # Raw extracted data (backup)
    raw_extracted_data = models.JSONField(default=dict)
    
    # File reference
    original_file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.original_file_name}"

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('APPLIED', 'Applied'),
        ('UNDER_REVIEW', 'Under Review'),
        ('INTERVIEW_SCHEDULED', 'Interview Scheduled'),
        ('INTERVIEWED', 'Interviewed'),
        ('REJECTED', 'Rejected'),
        ('ACCEPTED', 'Accepted'),
    ]
    
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    resume_data = models.ForeignKey(ResumeData, on_delete=models.CASCADE)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPLIED')
    
    # AI Matching Score
    ai_match_score = models.FloatField(null=True, blank=True)
    ai_match_details = models.JSONField(default=dict, blank=True)
    
    # Cover letter or additional notes
    cover_letter = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('job_posting', 'candidate')
    
    def __str__(self):
        return f"{self.candidate.username} -> {self.job_posting.title}"

class Interview(models.Model):
    INTERVIEW_TYPES = [
        ('PHONE', 'Phone'),
        ('VIDEO', 'Video Call'),
        ('ONSITE', 'On-site'),
        ('TECHNICAL', 'Technical'),
    ]
    
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('RESCHEDULED', 'Rescheduled'),
    ]
    
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE)
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    
    interview_type = models.CharField(max_length=20, choices=INTERVIEW_TYPES)
    scheduled_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    
    location = models.CharField(max_length=200, blank=True, null=True)
    meeting_link = models.URLField(blank=True, null=True)
    
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='SCHEDULED')
    notes = models.TextField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Interview: {self.application.candidate.username} for {self.application.job_posting.title}"

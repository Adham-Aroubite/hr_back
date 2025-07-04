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

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Company, UserProfile

# Add these new serializers to your existing serializers.py

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=UserProfile.USER_TYPES)
    company_code = serializers.CharField(write_only=True, required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm', 'user_type', 'company_code']
    
    def validate(self, attrs):
        # Check if passwords match
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        
        # If HR user, company_code is required
        if attrs['user_type'] == 'HR':
            if not attrs.get('company_code'):
                raise serializers.ValidationError("Company code is required for HR users")
            
            # Verify company code exists and is active
            try:
                company = Company.objects.get(registration_code=attrs['company_code'], is_active=True)
            except Company.DoesNotExist:
                raise serializers.ValidationError("Invalid or inactive company code")
            
            attrs['company'] = company
        
        return attrs
    
    def create(self, validated_data):
        # Remove non-user fields
        company = validated_data.pop('company', None)
        user_type = validated_data.pop('user_type')
        validated_data.pop('password_confirm')
        validated_data.pop('company_code', None)
        
        # Create user
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create user profile
        UserProfile.objects.create(
            user=user,
            user_type=user_type,
            company=company
        )
        
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            # Find user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError('Invalid email or password')
            
            # Authenticate user
            user = authenticate(username=user.username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password')
            
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include email and password')

class CurrentUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source='userprofile', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'profile']

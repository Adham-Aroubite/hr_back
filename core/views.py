
# ==== core/views.py (replace the existing content) ====
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Company, UserProfile, JobPosting, ResumeData, JobApplication, Interview
from .serializers import (
    CompanySerializer, UserProfileSerializer, JobPostingSerializer,
    ResumeDataSerializer, JobApplicationSerializer, InterviewSerializer
)

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # HR users can only see their own company
        user_profile = getattr(self.request.user, 'userprofile', None)
        if user_profile and user_profile.user_type == 'HR':
            return Company.objects.filter(id=user_profile.company.id)
        return Company.objects.none()

class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user_profile = getattr(self.request.user, 'userprofile', None)
        if user_profile and user_profile.user_type == 'HR':
            # HR users see jobs from their company
            return JobPosting.objects.filter(company=user_profile.company)
        elif user_profile and user_profile.user_type == 'CANDIDATE':
            # Candidates see all active jobs
            return JobPosting.objects.filter(status='ACTIVE')
        return JobPosting.objects.none()
    
    def perform_create(self, serializer):
        # Set the company and creator when creating a job
        user_profile = self.request.user.userprofile
        serializer.save(
            company=user_profile.company,
            created_by=self.request.user
        )
    
    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        """Get all applications for a specific job"""
        job = self.get_object()
        applications = JobApplication.objects.filter(job_posting=job)
        serializer = JobApplicationSerializer(applications, many=True)
        return Response(serializer.data)

class ResumeDataViewSet(viewsets.ModelViewSet):
    queryset = ResumeData.objects.all()
    serializer_class = ResumeDataSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own resume data
        return ResumeData.objects.filter(candidate=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(candidate=self.request.user)

class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user_profile = getattr(self.request.user, 'userprofile', None)
        if user_profile and user_profile.user_type == 'HR':
            # HR users see applications to their company's jobs
            return JobApplication.objects.filter(job_posting__company=user_profile.company)
        elif user_profile and user_profile.user_type == 'CANDIDATE':
            # Candidates see their own applications
            return JobApplication.objects.filter(candidate=self.request.user)
        return JobApplication.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(candidate=self.request.user)

class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user_profile = getattr(self.request.user, 'userprofile', None)
        if user_profile and user_profile.user_type == 'HR':
            # HR users see interviews for their company's applications
            return Interview.objects.filter(application__job_posting__company=user_profile.company)
        elif user_profile and user_profile.user_type == 'CANDIDATE':
            # Candidates see their own interviews
            return Interview.objects.filter(application__candidate=self.request.user)
        return Interview.objects.none()
    

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from .serializers import UserRegistrationSerializer, UserLoginSerializer, CurrentUserSerializer

# Add these new views to your existing views.py

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user (HR or Candidate)
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Create or get token
        token, created = Token.objects.get_or_create(user=user)
        
        # Get user profile info
        user_serializer = CurrentUserSerializer(user)
        
        return Response({
            'user': user_serializer.data,
            'token': token.key,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Login user with email and password
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Create or get token
        token, created = Token.objects.get_or_create(user=user)
        
        # Get user profile info
        user_serializer = CurrentUserSerializer(user)
        
        return Response({
            'user': user_serializer.data,
            'token': token.key,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_user(request):
    """
    Logout user by deleting their token
    """
    try:
        # Delete the user's token
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({'message': 'User was not logged in'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def current_user(request):
    """
    Get current user profile information
    """
    serializer = CurrentUserSerializer(request.user)
    return Response(serializer.data)

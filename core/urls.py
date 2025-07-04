
# ==== core/urls.py ====
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'companies', views.CompanyViewSet)
router.register(r'jobs', views.JobPostingViewSet)
router.register(r'applications', views.JobApplicationViewSet)
router.register(r'resume-data', views.ResumeDataViewSet)
router.register(r'interviews', views.InterviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'companies', views.CompanyViewSet)
router.register(r'jobs', views.JobPostingViewSet)
router.register(r'applications', views.JobApplicationViewSet)
router.register(r'resume-data', views.ResumeDataViewSet)
router.register(r'interviews', views.InterviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # Authentication endpoints
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', views.login_user, name='login'),
    path('auth/logout/', views.logout_user, name='logout'),
    path('auth/me/', views.current_user, name='current_user'),
]

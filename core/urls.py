
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
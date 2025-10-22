# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'profile', views.ProfileViewSet)
router.register(r'skills', views.SkillViewSet)
router.register(r'tools', views.ToolViewSet)
router.register(r'projects', views.ProjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('contact/', views.ContactFormView.as_view(), name='contact-form'),
]
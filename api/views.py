# api/views.py
from rest_framework import viewsets, permissions
from .models import Profile, Skill, Tool, Project
from rest_framework import viewsets, permissions, status 
from rest_framework.views import APIView           
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .serializers import (
    ProfileSerializer, SkillSerializer, ToolSerializer, ProjectSerializer
)

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Hanya admin yang bisa edit, user lain hanya bisa baca.
    """
    def has_permission(self, request, view):
        # Izin 'read' (GET, HEAD, OPTIONS) diizinkan untuk siapa saja
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Izin 'write' (POST, PUT, DELETE) hanya untuk admin
        return request.user and request.user.is_staff

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminOrReadOnly]

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAdminOrReadOnly]

class ToolViewSet(viewsets.ModelViewSet):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer
    permission_classes = [IsAdminOrReadOnly] 

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-id')
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminOrReadOnly] 

class ContactFormView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        nama = request.data.get('nama')
        email = request.data.get('email')
        pesan = request.data.get('pesan')

        if not nama or not email or not pesan:
            return Response(
                {"error": "Semua field harus diisi."},
                status=status.HTTP_400_BAD_REQUEST
            )

        subject = f"Pesan Portofolio Baru dari: {nama}"
        message_body = f"Nama: {nama}\nEmail: {email}\n\nPesan:\n{pesan}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [settings.ADMIN_EMAIL]

        try:
            send_mail(subject, message_body, from_email, recipient_list)
            return Response(
                {"success": "Pesan Anda berhasil terkirim!"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": f"Terjadi kesalahan: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
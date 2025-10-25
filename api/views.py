from rest_framework import viewsets, permissions, status 
from rest_framework.views import APIView           
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile, Skill, Tool, Project, ProjectImage
from .serializers import (
    ProfileSerializer, SkillSerializer, ToolSerializer, ProjectSerializer
)

class IsAdminOrReadOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user and request.user.is_staff

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    # TAMBAHKAN INI - untuk pass request ke serializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

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
    
    # TAMBAHKAN INI - untuk pass request ke serializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def perform_create(self, serializer):
        print("DEBUG (Create): Files yang diterima:", self.request.FILES)
        project = serializer.save()
        images_data = self.request.FILES.getlist('images')
        for image_file in images_data:
            ProjectImage.objects.create(project=project, image=image_file)
    
    def perform_update(self, serializer):
        print("DEBUG (Update): Files yang diterima:", self.request.FILES)
        project = serializer.save()
        images_data = self.request.FILES.getlist('images')
        for image_file in images_data:
            ProjectImage.objects.create(project=project, image=image_file)

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
                status=status.HTTP_200_OK  # FIX TYPO: HTTP_200_OK bukan HTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": f"Terjadi kesalahan: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

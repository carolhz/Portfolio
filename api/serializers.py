# api/serializers.py
from rest_framework import serializers
from .models import Profile, Skill, Tool, Project, ProjectImage

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'nama']

class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ['id', 'nama']

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image']

class ProjectSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), many=True
    )
    tools = serializers.PrimaryKeyRelatedField(
        queryset=Tool.objects.all(), many=True
    )
    
    images = ProjectImageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'judul', 'deskripsi', 'gambar_thumbnail', 
            'link_demo', 'link_repo', 'skills', 'tools',
            'role', 'images'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['skills'] = SkillSerializer(instance.skills, many=True).data
        representation['tools'] = ToolSerializer(instance.tools, many=True).data
        
        # --- INI ADALAH PERBAIKANNYA ---
        # Tambahkan baris ini untuk menyertakan gambar galeri
        representation['images'] = ProjectImageSerializer(instance.images, many=True).data
        
        return representation

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id', 'nama', 'deskripsi_singkat', 'deskripsi_lengkap',
            'foto', 'visi', 'misi', 'linkedin', 'github', 'email'
        ]
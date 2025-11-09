from rest_framework import serializers
from .models import Profile, Skill, Tool, Project, ProjectImage
import time

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'nama']


class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ['id', 'nama']


class ProjectImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectImage
        fields = ['id', 'image']
    
    def get_image(self, obj):
        if obj.image:
            url = str(obj.image.url)
            if url.startswith('http://'):
                url = url.replace('http://', 'https://')
            # ⚡ tambahin timestamp buat bypass cache
            url += f"?t={int(time.time())}"

            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(url)
            return url
        return None


class ProjectSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), many=True
    )
    tools = serializers.PrimaryKeyRelatedField(
        queryset=Tool.objects.all(), many=True
    )
    
    images = ProjectImageSerializer(many=True, read_only=True)
    gambar_thumbnail = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'judul', 'deskripsi', 'gambar_thumbnail', 
            'link_demo', 'link_repo', 'skills', 'tools',
            'role', 'images'
        ]
    
    def get_gambar_thumbnail(self, obj):
        if obj.gambar_thumbnail:
            url = str(obj.gambar_thumbnail.url)
            if url.startswith('http://'):
                url = url.replace('http://', 'https://')
            url += f"?t={int(time.time())}"

            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(url)
            return url
        return None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['skills'] = SkillSerializer(instance.skills, many=True).data
        representation['tools'] = ToolSerializer(instance.tools, many=True).data
        
        # Pass context ke ProjectImageSerializer
        representation['images'] = ProjectImageSerializer(
            instance.images, 
            many=True, 
            context=self.context
        ).data
        
        return representation


class ProfileSerializer(serializers.ModelSerializer):
    foto = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = [
            'id', 'nama', 'deskripsi_singkat', 'deskripsi_lengkap',
            'foto', 'visi', 'misi', 'linkedin', 'github', 'email'
        ]
    
    def get_foto(self, obj):
        if obj.foto:
            url = str(obj.foto.url)
            # 🔒 pastiin semua URL HTTPS (anti mixed-content)
            if url.startswith('http://'):
                url = url.replace('http://', 'https://')
            # ⚡ tambahin timestamp biar Cloudinary selalu kasih versi baru
            url += f"?t={int(time.time())}"

            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(url)
            return url
        return None

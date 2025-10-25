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
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectImage
        fields = ['id', 'image']
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                # Return full URL (Cloudinary akan otomatis kasih full URL)
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
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
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.gambar_thumbnail.url)
            return obj.gambar_thumbnail.url
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
            request = self.context.get('request')
            if request:
                # Return full URL (Cloudinary akan otomatis kasih full URL)
                return request.build_absolute_uri(obj.foto.url)
            return obj.foto.url
        return None

# api/serializers.py
from rest_framework import serializers
from .models import Profile, Skill, Tool, Project

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'nama']

class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ['id', 'nama']

class ProjectSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), many=True
    )
    tools = serializers.PrimaryKeyRelatedField(
        queryset=Tool.objects.all(), many=True
    )

    class Meta:
        model = Project
        fields = [
            'id', 'judul', 'deskripsi', 'gambar_thumbnail', 
            'link_demo', 'link_repo', 'skills', 'tools'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['skills'] = SkillSerializer(instance.skills, many=True).data
        representation['tools'] = ToolSerializer(instance.tools, many=True).data
        return representation


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
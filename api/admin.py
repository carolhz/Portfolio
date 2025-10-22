# api/admin.py
from django.contrib import admin
from .models import Profile, Skill, Tool, Project

admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Tool)
admin.site.register(Project)
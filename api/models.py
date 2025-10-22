# api/models.py
from django.db import models

class Profile(models.Model):
    nama = models.CharField(max_length=100)
    deskripsi_singkat = models.TextField(help_text="Paragraf singkat untuk di homepage")
    foto = models.ImageField(upload_to='profile/', blank=True, null=True)
    deskripsi_lengkap = models.TextField(help_text="Deskripsi untuk halaman 'About'")
    visi = models.TextField(blank=True)
    misi = models.TextField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.nama

class Skill(models.Model):
    nama = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nama

class Tool(models.Model):
    nama = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nama

class Project(models.Model):
    judul = models.CharField(max_length=200)
    deskripsi = models.TextField()
    gambar_thumbnail = models.ImageField(upload_to='projects/')
    link_demo = models.URLField(blank=True)
    link_repo = models.URLField(blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    tools = models.ManyToManyField(Tool, blank=True)
    
    def __str__(self):
        return self.judul
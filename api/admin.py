# api/admin.py
from django.contrib import admin
# Pastikan semua model diimpor
from .models import Profile, Skill, Tool, Project, ProjectImage

# Kelas Inline untuk Gambar
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1 # Slot untuk 1 gambar baru

# Kelas Admin kustom untuk Proyek
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]
    filter_horizontal = ('skills', 'tools')

# Daftarkan model-model Anda
admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Tool)
admin.site.register(ProjectImage) # Daftarkan juga model gambar

# Daftarkan Proyek menggunakan kelas Admin kustom
# (Baris admin.site.unregister(Project) yang error sudah dihapus)
# (Baris admin.site.register(Project) yang lama juga diganti dengan ini)
admin.site.register(Project, ProjectAdmin)
from django.contrib import admin
from .models import Profile, Project, Certificate, Skill, WorkExperience, Education

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display  = ['title', 'category', 'is_featured', 'order']
    list_editable = ['is_featured', 'order']
    list_filter   = ['category', 'is_featured']
    search_fields = ['title', 'tech_stack']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display  = ['name', 'category', 'proficiency', 'order']
    list_editable = ['proficiency', 'order']
    list_filter   = ['category']
    search_fields = ['name']

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display  = ['title', 'issuer', 'date_issued']
    list_filter   = ['issuer']
    search_fields = ['title', 'issuer']

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ['role', 'company', 'start_date', 'end_date']
    search_fields = ['role', 'company']

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'year_start', 'year_end']
    search_fields = ['degree', 'institution']

admin.site.register(Profile)

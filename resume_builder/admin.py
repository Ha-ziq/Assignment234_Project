from django.contrib import admin
from .models import (
    Resume, ResumeTemplate, WorkExperience, Education,
    Project, TechnicalSkill, Certification, Award,
    Language, Technology
)

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'visibility')
    search_fields = ('title', 'user__email')

@admin.register(ResumeTemplate)
class ResumeTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'format_type', 'version', 'is_active')
    list_filter = ('format_type', 'is_active')

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company', 'resume', 'start_date', 'end_date')
    list_filter = ('company',)
    search_fields = ('job_title',)

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'resume', 'start_date', 'end_date')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'resume', 'start_date', 'end_date', 'is_active')

@admin.register(TechnicalSkill)
class TechnicalSkillAdmin(admin.ModelAdmin):
    list_display = ('technology', 'resume', 'proficiency', 'years_experience')

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'issuer', 'resume', 'issue_date')

@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('title', 'issuer', 'resume', 'issue_date')

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'resume', 'proficiency')

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)

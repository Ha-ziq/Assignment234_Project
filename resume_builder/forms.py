# resume_builder/forms.py
from django import forms
from django.utils.text import slugify
from .models import (
    ResumeTemplate, Resume, ResumeSection, WorkExperience,
    TechnicalSkill, Education, Technology, Project,
    Certification, Award, Language
)

class ResumeTemplateForm(forms.ModelForm):
    class Meta:
        model = ResumeTemplate
        fields = ['name', 'description', 'format_type', 'version']

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'summary', 'tags', 'template', 'visibility']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'template': forms.Select(attrs={'class': 'form-select'}),
            'visibility': forms.Select(attrs={'class': 'form-select'}),
        }

# making technologies optional cant get rid of "" is invalid form in add_experince
class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['job_title', 'company', 'location', 'start_date', 'end_date', 'is_current', 'description', 'achievements', 'technologies']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['technologies'].required = False  # ✅ avoids validation error


class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['job_title', 'company', 'location', 'start_date', 'end_date', 'is_current', 'description', 'achievements', 'technologies']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['technologies'].required = False  # ✅ avoids validation error

class TechnicalSkillForm(forms.ModelForm):
    class Meta:
        model = TechnicalSkill
        fields = ['technology', 'proficiency', 'years_experience', 'last_used', 'project_count', 'is_visible']

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree', 'institution', 'location', 'start_date', 'end_date', 'gpa', 'description', 'is_visible']
        widgets = {
            'degree': forms.TextInput(attrs={'class': 'form-control'}),
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gpa': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_visible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class TechnologyForm(forms.ModelForm):
    class Meta:
        model = Technology
        fields = ['name', 'category', 'icon']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['name', 'issuer', 'issue_date', 'expiration_date', 'credential_id', 'verification_url', 'skills']

class AwardForm(forms.ModelForm):
    class Meta:
        model = Award
        fields = ['title', 'issuer', 'issue_date', 'category', 'description', 'impact_metrics', 'is_visible']

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['name', 'proficiency', 'certification', 'is_visible']
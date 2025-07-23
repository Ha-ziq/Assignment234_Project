# Python
from django.urls import path
from .views import (
    WorkExperienceListView, WorkExperienceCreateView, WorkExperienceUpdateView,
    WorkExperienceDeleteView, WorkExperienceDetailView, EducationListView, EducationDetailView,
    EducationCreateView, EducationUpdateView, EducationDeleteView,ResumePreviewView,ResumeListView,
    ResumeCreateView,TechnicalSkillListView,TechnicalSkillCreateView,TechnicalSkillDetailView,
    TechnicalSkillUpdateView,TechnicalSkillDeleteView,ProjectListView, ProjectDetailView,
    ProjectCreateView,ProjectUpdateView, ProjectDeleteView,CertificationListView,
    CertificationCreateView,CertificationDetailView,CertificationUpdateView,CertificationDeleteView,
    AwardListView, AwardCreateView, AwardDetailView, AwardUpdateView, AwardDeleteView,
    LanguageListView, LanguageCreateView, LanguageDetailView, LanguageUpdateView, 
    LanguageDeleteView, ResumeDeleteView, ResumeDownloadView,TemplatePreviewView

)


urlpatterns = [
#url for resume
  
    path('resumes/', ResumeListView.as_view(), name='resume_list'),
    path('resumes/add/', ResumeCreateView.as_view(), name='resume_create'),
 # URL for the resume list page
    path('resumes/', ResumeListView.as_view(), name='resume_list'),
    
#url for resume    
   path('resume/<int:pk>/preview/', ResumePreviewView.as_view(), name='resume_preview'),
   path('resumes/<int:pk>/delete/', ResumeDeleteView.as_view(), name='resume_delete'),
    # other paths...

#urls for work experience
    path('work-experience/', WorkExperienceListView.as_view(), name='work_experience_list'),
    path('work-experience/add/', WorkExperienceCreateView.as_view(), name='work_experience_create'),
    path('work-experience/<int:pk>/edit/', WorkExperienceUpdateView.as_view(), name='work_experience_update'),
    path('work-experience/<int:pk>/delete/', WorkExperienceDeleteView.as_view(), name='work_experience_delete'),
    path('work-experience/<int:pk>/', WorkExperienceDetailView.as_view(), name='work_experience_detail'),
#urls for education
    path('education/', EducationListView.as_view(), name='education_list'),
    path('education/add/', EducationCreateView.as_view(), name='education_create'),
    path('education/<int:pk>/', EducationDetailView.as_view(), name='education_detail'),
    path('education/<int:pk>/edit/', EducationUpdateView.as_view(), name='education_update'),
    path('education/<int:pk>/delete/', EducationDeleteView.as_view(), name='education_delete'),
#urls for technical skills
    path('skills/', TechnicalSkillListView.as_view(), name='technical_skill_list'),
    path('skills/add/', TechnicalSkillCreateView.as_view(), name='technical_skill_create'),
    path('skills/<int:pk>/', TechnicalSkillDetailView.as_view(), name='technical_skill_detail'),
    path('skills/<int:pk>/edit/', TechnicalSkillUpdateView.as_view(), name='technical_skill_update'),
    path('skills/<int:pk>/delete/', TechnicalSkillDeleteView.as_view(), name='technical_skill_delete'),
# URLs for projects
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/add/', ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('projects/<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_update'),
    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
# URLs for certificates
    path('certifications/', CertificationListView.as_view(), name='certification_list'),
    path('certifications/add/', CertificationCreateView.as_view(), name='certification_create'),
    path('certifications/<int:pk>/', CertificationDetailView.as_view(), name='certification_detail'),
    path('certifications/<int:pk>/edit/', CertificationUpdateView.as_view(), name='certification_update'),
    path('certifications/<int:pk>/delete/', CertificationDeleteView.as_view(), name='certification_delete'),
# Award URLs
    path('awards/', AwardListView.as_view(), name='award_list'),
    path('awards/add/', AwardCreateView.as_view(), name='award_create'),
    path('awards/<int:pk>/', AwardDetailView.as_view(), name='award_detail'),
    path('awards/<int:pk>/edit/', AwardUpdateView.as_view(), name='award_update'),
    path('awards/<int:pk>/delete/', AwardDeleteView.as_view(), name='award_delete'),
# Language URLs
    path('languages/', LanguageListView.as_view(), name='language_list'),
    path('languages/add/', LanguageCreateView.as_view(), name='language_create'),
    path('languages/<int:pk>/', LanguageDetailView.as_view(), name='language_detail'),
    path('languages/<int:pk>/edit/', LanguageUpdateView.as_view(), name='language_update'),
    path('languages/<int:pk>/delete/', LanguageDeleteView.as_view(), name='language_delete'),

#resume download url
    path('resume/<slug:slug>/download/', ResumeDownloadView.as_view(), name='resume_download'),

#template design preview url
path("resume/template/preview/", TemplatePreviewView.as_view(), name="template_preview"),
]


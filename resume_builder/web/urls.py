# Python
from django.urls import path
from .views import (
    WorkExperienceListView, WorkExperienceCreateView, WorkExperienceUpdateView,
    WorkExperienceDeleteView, WorkExperienceDetailView, EducationListView, EducationDetailView,
    EducationCreateView, EducationUpdateView, EducationDeleteView,ResumePreviewView,ResumeListView,
    ResumeCreateView
)

urlpatterns = [
#url for resume
    path('resume/<int:pk>/preview/', ResumePreviewView.as_view(), name='resume_preview'),
    path('resumes/', ResumeListView.as_view(), name='resume_list'),
    path('resumes/add/', ResumeCreateView.as_view(), name='resume_create'),

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
]


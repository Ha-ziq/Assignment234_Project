# Python
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.text import slugify
import re
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from resume_builder.models import WorkExperience,Resume,Education,TechnicalSkill,Project,Certification,Award,Language,ResumeTemplate
from resume_builder.forms import WorkExperienceForm,EducationForm,ResumeForm,TechnicalSkillForm,ProjectForm,CertificationForm,AwardForm,LanguageForm
from django.http import HttpResponse,FileResponse,Http404
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.shortcuts import get_object_or_404
from io import BytesIO



#view for resume
class ResumePreviewView(LoginRequiredMixin, DetailView):
    model = Resume
    context_object_name = 'resume'

    def get_template_names(self):
        template_type = self.get_object().template.format_type.lower()
        return [f"resume_builder/resume/{template_type}_preview.html"]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    
class ResumeListView(LoginRequiredMixin, ListView):
    model = Resume
    template_name = 'resume_builder/resume/resume_list.html'
    context_object_name = 'resumes'

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

class ResumeDeleteView(LoginRequiredMixin, DeleteView):
    model = Resume
    success_url = reverse_lazy('resume_list')

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)
    
class ResumeCreateView(LoginRequiredMixin, CreateView):
    model = Resume
    form_class = ResumeForm
    template_name = 'resume_builder/resume/resume_form.html'
    success_url = reverse_lazy('resume_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['templates'] = ResumeTemplate.objects.filter(is_active=True)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user

        # Generate slug from title
        if not form.instance.slug:
            form.instance.slug = slugify(form.instance.title)

        # Set default language if not provided
        if not form.instance.language:
            form.instance.language = 'en'

        return super().form_valid(form)

    def form_invalid(self, form):
        print("❌ Resume form invalid:", form.errors)
        return super().form_invalid(form)

#resume download view

class ResumeDownloadView(View):
    def get(self, request, slug):
        resume = get_object_or_404(Resume, slug=slug, user=request.user)
        template_name_from_db = resume.template.name if resume.template else None
        print("Resume template in DB:", template_name_from_db)

        # Template mapping
        TEMPLATE_MAP = {
            "Classic": "classic_preview.html",
            "Modern": "modern_preview.html",
            "Technical": "technical_preview.html",
            "Creative": "creative_preview.html",
        }

        file_name = TEMPLATE_MAP.get(template_name_from_db)
        if not file_name:
            raise Http404(f"No template found for: {template_name_from_db}")

        # Render HTML
        template_path = f"resume_builder/resume/{file_name}"
        html_string = render_to_string(template_path, {"resume": resume})

        # Generate PDF and write to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(temp_file.name)
            temp_file.flush()

        # Return downloadable response
        return FileResponse(
            open(temp_file.name, 'rb'),
            as_attachment=True,
            filename=f"{resume.slug}.pdf",
            content_type='application/pdf'
        )


  
       


#views for work exoerience

class WorkExperienceListView(LoginRequiredMixin, ListView):
    model = WorkExperience
    template_name = 'resume_builder/work_experience/work_experience_list.html'
    context_object_name = 'experiences'

    def get_queryset(self):
        return WorkExperience.objects.filter(resume__user=self.request.user)

class WorkExperienceCreateView(LoginRequiredMixin, CreateView):
    model = WorkExperience
    form_class = WorkExperienceForm
    template_name = 'resume_builder/work_experience/work_experience_form.html'
    success_url = reverse_lazy('work_experience_list')

    def form_valid(self, form):
        # Automatically assign resume that belongs to the user
        user_resumes = Resume.objects.filter(user=self.request.user)
        if not user_resumes.exists():
            form.add_error(None, "You must create a resume before adding work experience.")
            return self.form_invalid(form)

        form.instance.resume = user_resumes.first()
        return super().form_valid(form)


class WorkExperienceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = WorkExperience
    form_class = WorkExperienceForm
    template_name = 'resume_builder/work_experience/work_experience_form.html'
    success_url = reverse_lazy('work_experience_list')

    def test_func(self):
        return self.get_object().resume.user == self.request.user

class WorkExperienceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = WorkExperience
    template_name = 'resume_builder/work_experience/work_experience_confirm_delete.html'
    success_url = reverse_lazy('work_experience_list')

    def test_func(self):
        return self.get_object().resume.user == self.request.user

class WorkExperienceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = WorkExperience
    template_name = 'resume_builder/work_experience/work_experience_detail.html'
    context_object_name = 'experience'

    def test_func(self):
        return self.get_object().resume.user == self.request.user
    

#view for education



class EducationListView(LoginRequiredMixin, ListView):
    model = Education
    template_name = 'resume_builder/education/education_list.html'
    context_object_name = 'educations'

    def get_queryset(self):
        return Education.objects.filter(resume__user=self.request.user)

class EducationDetailView(LoginRequiredMixin, DetailView):
    model = Education
    template_name = 'resume_builder/education/education_detail.html'

    def get_queryset(self):
        return Education.objects.filter(resume__user=self.request.user)

class EducationCreateView(LoginRequiredMixin, CreateView):
    model = Education
    form_class = EducationForm
    template_name = 'resume_builder/education/education_form.html'
    success_url = reverse_lazy('education_list')

    def form_valid(self, form):
        # Automatically assign resume
        user_resumes = Resume.objects.filter(user=self.request.user)
        if not user_resumes.exists():
            form.add_error(None, "You must create a resume before adding education.")
            return self.form_invalid(form)

        form.instance.resume = user_resumes.first()  # assign resume directly
        return super().form_valid(form)


class EducationUpdateView(LoginRequiredMixin, UpdateView):
    model = Education
    form_class = EducationForm
    template_name = 'resume_builder/education/education_form.html'
    success_url = reverse_lazy('education_list')

    def get_queryset(self):
        return Education.objects.filter(resume__user=self.request.user)

class EducationDeleteView(LoginRequiredMixin, DeleteView):
    model = Education
    template_name = 'resume_builder/education/education_confirm_delete.html'
    success_url = reverse_lazy('education_list')

    def get_queryset(self):
        return Education.objects.filter(resume__user=self.request.user)


#technical skills views

# TECHNICAL SKILL VIEWS
class TechnicalSkillListView(LoginRequiredMixin, ListView):
    model = TechnicalSkill
    template_name = 'resume_builder/technical_skill/technical_skill_list.html'
    context_object_name = 'skills'

    def get_queryset(self):
        return TechnicalSkill.objects.filter(resume__user=self.request.user)

class TechnicalSkillCreateView(LoginRequiredMixin, CreateView):
    model = TechnicalSkill
    form_class = TechnicalSkillForm
    template_name = 'resume_builder/technical_skill/technical_skill_form.html'
    success_url = reverse_lazy('technical_skill_list')

    def form_valid(self, form):
        user_resumes = Resume.objects.filter(user=self.request.user)
        if not user_resumes.exists():
            form.add_error(None, "You must create a resume first.")
            return self.form_invalid(form)
        form.instance.resume = user_resumes.first()
        return super().form_valid(form)

class TechnicalSkillUpdateView(LoginRequiredMixin, UpdateView):
    model = TechnicalSkill
    form_class = TechnicalSkillForm
    template_name = 'resume_builder/technical_skill/technical_skill_form.html'
    success_url = reverse_lazy('technical_skill_list')

    def get_queryset(self):
        return TechnicalSkill.objects.filter(resume__user=self.request.user)

class TechnicalSkillDeleteView(LoginRequiredMixin, DeleteView):
    model = TechnicalSkill
    template_name = 'resume_builder/technical_skill/technical_skill_confirm_delete.html'
    success_url = reverse_lazy('technical_skill_list')

    def get_queryset(self):
        return TechnicalSkill.objects.filter(resume__user=self.request.user)

class TechnicalSkillDetailView(LoginRequiredMixin, DetailView):
    model = TechnicalSkill
    template_name = 'resume_builder/technical_skill/technical_skill_detail.html'
    context_object_name = 'skill'

    def get_queryset(self):
        return TechnicalSkill.objects.filter(resume__user=self.request.user)

#views for projects



class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'resume_builder/project/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(resume__user=self.request.user)

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'resume_builder/project/project_detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        return Project.objects.filter(resume__user=self.request.user)

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'resume_builder/project/project_form.html'
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        user_resumes = Resume.objects.filter(user=self.request.user)
        if not user_resumes.exists():
            form.add_error(None, "You must create a resume before adding projects.")
            return self.form_invalid(form)

        form.instance.resume = user_resumes.first()
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'resume_builder/project/project_form.html'
    success_url = reverse_lazy('project_list')

    def test_func(self):
        return self.get_object().resume.user == self.request.user

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'resume_builder/project/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')

    def test_func(self):
        return self.get_object().resume.user == self.request.user

#views for certificates
# views.py


class CertificationListView(LoginRequiredMixin, ListView):
    model = Certification
    template_name = 'resume_builder/certification/certification_list.html'
    context_object_name = 'certifications'

    def get_queryset(self):
        return Certification.objects.filter(resume__user=self.request.user)

class CertificationDetailView(LoginRequiredMixin, DetailView):
    model = Certification
    template_name = 'resume_builder/certification/certification_detail.html'
    context_object_name = 'certification'

    def get_queryset(self):
        return Certification.objects.filter(resume__user=self.request.user)

class CertificationCreateView(LoginRequiredMixin, CreateView):
    model = Certification
    form_class = CertificationForm
    template_name = 'resume_builder/certification/certification_form.html'
    success_url = reverse_lazy('certification_list')

    def form_valid(self, form):
        user_resumes = Resume.objects.filter(user=self.request.user)
        if not user_resumes.exists():
            form.add_error(None, "You must create a resume first.")
            return self.form_invalid(form)
        form.instance.resume = user_resumes.first()
        return super().form_valid(form)

class CertificationUpdateView(LoginRequiredMixin, UpdateView):
    model = Certification
    form_class = CertificationForm
    template_name = 'resume_builder/certification/certification_form.html'
    success_url = reverse_lazy('certification_list')

    def get_queryset(self):
        return Certification.objects.filter(resume__user=self.request.user)

class CertificationDeleteView(LoginRequiredMixin, DeleteView):
    model = Certification
    template_name = 'resume_builder/certification/certification_confirm_delete.html'
    success_url = reverse_lazy('certification_list')

    def get_queryset(self):
        return Certification.objects.filter(resume__user=self.request.user)

# AWARD VIEWS
class AwardListView(LoginRequiredMixin, ListView):
    model = Award
    template_name = 'resume_builder/award/award_list.html'
    context_object_name = 'awards'

    def get_queryset(self):
        return Award.objects.filter(resume__user=self.request.user)

class AwardDetailView(LoginRequiredMixin, DetailView):
    model = Award
    template_name = 'resume_builder/award/award_detail.html'
    context_object_name = 'award'

    def get_queryset(self):
        return Award.objects.filter(resume__user=self.request.user)

class AwardCreateView(LoginRequiredMixin, CreateView):
    model = Award
    form_class = AwardForm
    template_name = 'resume_builder/award/award_form.html'
    success_url = reverse_lazy('award_list')

    def form_valid(self, form):
        resume = Resume.objects.filter(user=self.request.user).first()
        if not resume:
            form.add_error(None, "Create a resume first.")
            return self.form_invalid(form)
        form.instance.resume = resume
        return super().form_valid(form)

class AwardUpdateView(LoginRequiredMixin, UpdateView):
    model = Award
    form_class = AwardForm
    template_name = 'resume_builder/award/award_form.html'
    success_url = reverse_lazy('award_list')

    def get_queryset(self):
        return Award.objects.filter(resume__user=self.request.user)

class AwardDeleteView(LoginRequiredMixin, DeleteView):
    model = Award
    template_name = 'resume_builder/award/award_confirm_delete.html'
    success_url = reverse_lazy('award_list')

    def get_queryset(self):
        return Award.objects.filter(resume__user=self.request.user)

# LANGUAGE VIEWS
class LanguageListView(LoginRequiredMixin, ListView):
    model = Language
    template_name = 'resume_builder/language/language_list.html'
    context_object_name = 'languages'

    def get_queryset(self):
        return Language.objects.filter(resume__user=self.request.user)

class LanguageDetailView(LoginRequiredMixin, DetailView):
    model = Language
    template_name = 'resume_builder/language/language_detail.html'
    context_object_name = 'language'

    def get_queryset(self):
        return Language.objects.filter(resume__user=self.request.user)

class LanguageCreateView(LoginRequiredMixin, CreateView):
    model = Language
    form_class = LanguageForm
    template_name = 'resume_builder/language/language_form.html'
    success_url = reverse_lazy('language_list')

    def form_valid(self, form):
        resume = Resume.objects.filter(user=self.request.user).first()
        if not resume:
            form.add_error(None, "Create a resume first.")
            return self.form_invalid(form)
        form.instance.resume = resume
        return super().form_valid(form)

class LanguageUpdateView(LoginRequiredMixin, UpdateView):
    model = Language
    form_class = LanguageForm
    template_name = 'resume_builder/language/language_form.html'
    success_url = reverse_lazy('language_list')

    def get_queryset(self):
        return Language.objects.filter(resume__user=self.request.user)

class LanguageDeleteView(LoginRequiredMixin, DeleteView):
    model = Language
    template_name = 'resume_builder/language/language_confirm_delete.html'
    success_url = reverse_lazy('language_list')

    def get_queryset(self):
        return Language.objects.filter(resume__user=self.request.user)

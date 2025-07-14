# Python
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from resume_builder.models import WorkExperience,Resume,Education
from resume_builder.forms import WorkExperienceForm,EducationForm,ResumeForm


#view for resume
class ResumePreviewView(LoginRequiredMixin, DetailView):
    model = Resume
    template_name = 'resume_builder/resume_preview.html'
    context_object_name = 'resume'

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)
    
class ResumeListView(LoginRequiredMixin, ListView):
    model = Resume
    template_name = 'resume_builder/resume/resume_list.html'
    context_object_name = 'resumes'

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

class ResumeCreateView(LoginRequiredMixin, CreateView):
    model = Resume
    form_class = ResumeForm
    template_name = 'resume_builder/resume/resume_form.html'
    success_url = reverse_lazy('resume_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


#views for work exoerience

class WorkExperienceListView(LoginRequiredMixin, ListView):
    model = WorkExperience
    template_name = 'resume_builder/work_experience/work_experience_list.html'
    context_object_name = 'experiences'

    def get_queryset(self):
        return WorkExperience.objects.filter(resume__user=self.request.user)

# class WorkExperienceCreateView(LoginRequiredMixin, CreateView):
#     model = WorkExperience
#     form_class = WorkExperienceForm
#     template_name = 'resume_builder/work_experience/work_experience_form.html'
#     success_url = reverse_lazy('work_experience_list')

#     def form_valid(self, form):
#         # Ensure the resume belongs to the user
#         resume = form.cleaned_data['resume']
#         if resume.user != self.request.user:
#             form.add_error('resume', 'You do not own this resume.')
#             return self.form_invalid(form)
#         return super().form_valid(form)

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
        resume = form.cleaned_data['resume']
        if resume.user != self.request.user:
            form.add_error('resume', 'Invalid resume ownership.')
            return self.form_invalid(form)
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

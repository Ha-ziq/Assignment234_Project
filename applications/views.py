from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def classic_preview(request):
    return render(request, 'resume/classic_preview.html')

def modern_preview(request):
    return render(request, 'resume/modern_preview.html')

def creative_preview(request):
    return render(request, 'resume/creative_preview.html')
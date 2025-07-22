from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/web/accounts/login/')
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required(login_url='/web/accounts/login/')
def classic_preview(request):
    return render(request, 'resume/classic_preview.html')

@login_required(login_url='/web/accounts/login/')
def modern_preview(request):
    return render(request, 'resume/modern_preview.html')

@login_required(login_url='/web/accounts/login/')
def creative_preview(request):
    return render(request, 'resume/creative_preview.html')

@login_required(login_url='/web/accounts/login/')
def technical_preview(request):
    return render(request, 'resume/technical_preview.html')
import threading
from django.shortcuts import render, redirect, get_object_or_400
from django.contrib.admin.views.decorators import staff_member_required
from django.core.management import call_command
from django.contrib import messages

from .models import Profile, Project, Certificate, Skill, WorkExperience, Education
from .forms import ProfileForm

# =============================================================================
# PUBLIC PORTFOLIO VIEWS
# =============================================================================

def index(request):
    profile = Profile.objects.first()
    featured_projects = Project.objects.filter(is_featured=True).order_by('order', '-created_at')
    certificates = Certificate.objects.all().order_by('-date_issued')
    skills = Skill.objects.all().order_by('category', 'order')
    experiences = WorkExperience.objects.all().order_by('-start_date')[:3]  # Show recent 3

    context = {
        'profile': profile,
        'featured_projects': featured_projects,
        'certificates': certificates,
        'skills': skills,
        'experiences': experiences,
    }
    return render(request, 'portfolio/index.html', context)


def about(request):
    profile = Profile.objects.first()
    skills = Skill.objects.all().order_by('category', 'order')
    experiences = WorkExperience.objects.all().order_by('-start_date')
    education = Education.objects.all().order_by('-year_start')

    context = {
        'profile': profile,
        'skills': skills,
        'experiences': experiences,
        'education': education,
    }
    return render(request, 'portfolio/about.html', context)


def projects(request):
    profile = Profile.objects.first()
    all_projects = Project.objects.all().order_by('order', '-created_at')
    
    # Extract active categories that exist in projects to filter nicely
    categories = Project.CATEGORY

    context = {
        'profile': profile,
        'projects': all_projects,
        'categories': categories,
    }
    return render(request, 'portfolio/projects.html', context)


def project_detail(request, pk):
    profile = Profile.objects.first()
    project = get_object_or_400(Project, pk=pk)
    
    # Recommendation: other projects
    other_projects = Project.objects.exclude(pk=pk).order_by('?')[:3]

    context = {
        'profile': profile,
        'project': project,
        'other_projects': other_projects,
    }
    return render(request, 'portfolio/project_detail.html', context)


# =============================================================================
# CUSTOM CMS PORTFOLIO PANEL VIEWS
# =============================================================================

@staff_member_required
def panel_dashboard(request):
    profile = Profile.objects.first()
    projects_count = Project.objects.count()
    certs_count = Certificate.objects.count()
    skills_count = Skill.objects.count()
    exp_count = WorkExperience.objects.count()
    edu_count = Education.objects.count()

    context = {
        'profile': profile,
        'projects_count': projects_count,
        'certs_count': certs_count,
        'skills_count': skills_count,
        'exp_count': exp_count,
        'edu_count': edu_count,
    }
    return render(request, 'portfolio/panel/dashboard.html', context)


@staff_member_required
def panel_settings(request):
    profile = Profile.objects.first()
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '⚙️ Pengaturan profil berhasil diperbarui! Silakan klik Publish untuk menyinkronkan ke GitHub Pages.')
            return redirect('panel_dashboard')
    else:
        form = ProfileForm(instance=profile)

    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'portfolio/panel/settings.html', context)


@staff_member_required
def publish_to_github(request):
    if request.method == 'POST':
        try:
            # We execute it inside a background thread so the HTTP request
            # does not timeout waiting for Git operations to complete
            def do_publish():
                call_command('publish_static')
            
            t = threading.Thread(target=do_publish)
            t.start()
            messages.success(request, '🚀 Proses sinkronisasi dimulai! Portfolio statis Anda sedang dibuat dan di-push ke GitHub Pages. Mohon tunggu 1-2 menit hingga GitHub selesai mendeploy.')
        except Exception as e:
            messages.error(request, f'❌ Terjadi kesalahan saat memicu proses publish: {str(e)}')
            
    return redirect('panel_dashboard')

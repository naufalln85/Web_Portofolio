from django.urls import path
from . import views

urlpatterns = [
    # Public Client Portfolio Routes
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),

    # Custom CMS Admin Control Panel Routes
    path('panel/', views.panel_dashboard, name='panel_dashboard'),
    path('panel/settings/', views.panel_settings, name='panel_settings'),
    path('panel/publish/', views.publish_to_github, name='publish'),
]

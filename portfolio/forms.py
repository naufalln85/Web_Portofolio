from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'name', 'title', 'tagline', 'bio', 'photo', 'email', 
            'github_url', 'linkedin_url', 'cv_file', 'accent_color'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Lengkap'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pekerjaan (e.g. Web Developer)'}),
            'tagline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Slogan singkat (Hero section)'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Biografi detail...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/username'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/username'}),
            'accent_color': forms.TextInput(attrs={'class': 'form-control color-picker-input', 'type': 'color'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'cv_file': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

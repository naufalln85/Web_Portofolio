import os
import shutil
import subprocess
from datetime import datetime
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.conf import settings
from portfolio.models import Profile, Project, Certificate, Skill, WorkExperience, Education

class Command(BaseCommand):
    help = 'Mengekspor halaman Django menjadi HTML statis dan mempublikasikannya ke GitHub Pages'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Memulai ekspor portfolio statis...')
        export_dir = settings.STATIC_EXPORT_DIR

        # 1. Pastikan GITHUB environment terisi sebelum mengekspor
        token = os.environ.get('GITHUB_TOKEN')
        repo = os.environ.get('GITHUB_REPO')
        if not token or not repo:
            self.stdout.write(self.style.ERROR(
                '❌ GITHUB_TOKEN atau GITHUB_REPO belum dikonfigurasi di file .env!\n'
                'Harap ikuti langkah di panduan untuk membuat Token dan melengkapi .env.'
            ))
            raise ValueError("Token GitHub atau Repo tidak ditemukan dalam Environment Variables.")

        # 2. Bersihkan dan inisialisasi folder export
        self.stdout.write('🧹 Mengosongkan folder export...')
        self._init_export_dir(export_dir)

        # 3. Ambil data database
        self.stdout.write('📦 Mengambil data konten dari database...')
        context = self._get_context()

        # 4. Render file-file utama
        self.stdout.write('🎨 Merender template Django menjadi HTML statis...')
        self._render_pages(export_dir, context)

        # 5. Salin media assets dan static files
        self.stdout.write('📂 Menyalin static dan media assets...')
        self._copy_assets(export_dir)

        # 6. Push ke GitHub Pages
        self.stdout.write('📤 Melakukan git push force ke GitHub Pages...')
        self._git_push(export_dir, token, repo)

        self.stdout.write(self.style.SUCCESS('✅ Sinkronisasi berhasil! Portfoliomu telah dipublish ke GitHub Pages.'))

    def _init_export_dir(self, export_dir):
        if os.path.exists(export_dir):
            try:
                shutil.rmtree(export_dir)
            except PermissionError:
                # Windows handling fallback
                subprocess.run(['rmdir', '/s', '/q', export_dir], shell=True)
                
        os.makedirs(export_dir, exist_ok=True)
        
        # Inisialisasi git local repositori di dalam target export
        subprocess.run(['git', 'init'], cwd=export_dir, stdout=subprocess.DEVNULL)

    def _get_context(self):
        return {
            'profile':      Profile.objects.first(),
            'projects':     Project.objects.all().order_by('order', '-created_at'),
            'featured_projects': Project.objects.filter(is_featured=True).order_by('order', '-created_at'),
            'certificates': Certificate.objects.all().order_by('-date_issued'),
            'skills':       Skill.objects.all().order_by('category', 'order'),
            'experiences':  WorkExperience.objects.all().order_by('-start_date'),
            'education':    Education.objects.all().order_by('-year_start'),
            'published_at': datetime.now().strftime('%d %B %Y %H:%M'),
            'is_static':    True,  # Tells template to render links for static files (.html)
            'url_prefix':   '',    # Prefix for static links (empty at root level)
        }

    def _render_pages(self, export_dir, context):
        pages = {
            'index.html':    'portfolio/index.html',
            'about.html':    'portfolio/about.html',
            'projects.html': 'portfolio/projects.html',
        }
        for filename, template in pages.items():
            html = render_to_string(template, context)
            with open(os.path.join(export_dir, filename), 'w', encoding='utf-8') as f:
                f.write(html)
            self.stdout.write(f'  ✓ Rendered {filename}')

        # Render halaman detail untuk tiap project
        projects_dir = os.path.join(export_dir, 'projects')
        os.makedirs(projects_dir, exist_ok=True)
        
        for project in context['projects']:
            ctx = {**context, 'project': project, 'url_prefix': '../'}
            html = render_to_string('portfolio/project_detail.html', ctx)
            # Link file static diletakkan di projects/<id>.html
            with open(os.path.join(projects_dir, f'{project.pk}.html'), 'w', encoding='utf-8') as f:
                f.write(html)
            self.stdout.write(f'  ✓ Rendered projects/{project.pk}.html')

    def _copy_assets(self, export_dir):
        # 1. Salin media uploads (foto, cv, dll)
        if os.path.exists(settings.MEDIA_ROOT) and os.listdir(settings.MEDIA_ROOT):
            shutil.copytree(settings.MEDIA_ROOT, os.path.join(export_dir, 'media'), dirs_exist_ok=True)
            self.stdout.write('  ✓ Media assets disalin.')
        else:
            self.stdout.write('  ⚠️  Media uploads kosong atau tidak ditemukan. Melewati.')

        # 2. Salin static assets (CSS, JS, Fonts dari collectstatic)
        if os.path.exists(settings.STATIC_ROOT) and os.listdir(settings.STATIC_ROOT):
            shutil.copytree(settings.STATIC_ROOT, os.path.join(export_dir, 'static'), dirs_exist_ok=True)
            self.stdout.write('  ✓ Static assets disalin.')
        else:
            self.stdout.write('  ⚠️  Staticfiles kosong. Harap pastikan python manage.py collectstatic dijalankan.')

    def _git_push(self, export_dir, token, repo):
        branch = os.environ.get('GITHUB_BRANCH', 'gh-pages')
        # URL dengan Token Autentikasi untuk automatic push
        remote = f'https://{token}@github.com/{repo}.git'

        cmds = [
            ['git', 'config', 'user.email', 'deploy@portfolio.local'],
            ['git', 'config', 'user.name',  'Portfolio Autodeploy Bot'],
            ['git', 'add', '.'],
            ['git', 'commit', '-m', f'Auto publish: {datetime.now():%Y-%m-%d %H:%M:%S}'],
            ['git', 'push', '--force', remote, f'HEAD:{branch}'],
        ]
        
        for cmd in cmds:
            # We hide the remote URL in logs for security (protects token from leaking in output)
            log_cmd = [arg if 'github.com' not in arg else 'https://[TOKEN]@github.com/...' for arg in cmd]
            self.stdout.write(f'  Menjalankan: {" ".join(log_cmd)}')
            
            result = subprocess.run(cmd, cwd=export_dir, capture_output=True)
            if result.returncode != 0:
                error_str = result.stderr.decode()
                # Clean up GITHUB_TOKEN from error messages if it leaks
                clean_error = error_str.replace(token, '******') if token in error_str else error_str
                
                # Check for harmless empty commits
                if 'nothing to commit' in clean_error or 'no changes added to commit' in clean_error:
                    self.stdout.write('  ✓ Git: Tidak ada perubahan untuk dicommit.')
                    continue
                    
                raise RuntimeError(f'Git error: {clean_error}')

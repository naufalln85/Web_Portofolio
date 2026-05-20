from django.db import models

class Profile(models.Model):
    name         = models.CharField(max_length=100)
    title        = models.CharField(max_length=200, help_text="Contoh: Full-Stack Developer")
    bio          = models.TextField()
    photo        = models.ImageField(upload_to='profile/')
    email        = models.EmailField()
    github_url   = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    cv_file      = models.FileField(upload_to='cv/', blank=True)
    tagline      = models.CharField(max_length=300, blank=True)
    accent_color = models.CharField(max_length=7, default='#00C978', help_text="Format HEX, Contoh: #00C978")

    def __str__(self):
        return self.name


class Project(models.Model):
    CATEGORY = [
        ('web',    'Web Application'),
        ('mobile', 'Mobile App'),
        ('brand',  'Brand Identity'),
        ('data',   'Data Science'),
    ]
    title       = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail   = models.ImageField(upload_to='projects/')
    tech_stack  = models.CharField(max_length=300, help_text="Pisahkan dengan koma, contoh: Django, React, Postgres")
    category    = models.CharField(max_length=20, choices=CATEGORY)
    live_url    = models.URLField(blank=True)
    repo_url    = models.URLField(blank=True)
    order       = models.IntegerField(default=0, help_text="Urutan tampilan (angka terkecil tampil duluan)")
    is_featured = models.BooleanField(default=False, help_text="Tampilkan di beranda depan sebagai unggulan")
    created_at  = models.DateTimeField(auto_now_add=True)

    def tech_list(self):
        """Helper to split tech_stack string into a list of tags"""
        return [tech.strip() for tech in self.tech_stack.split(',') if tech.strip()]

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


class Certificate(models.Model):
    title          = models.CharField(max_length=200)
    issuer         = models.CharField(max_length=200, help_text="Penerbit sertifikat, contoh: Dicoding, Coursera")
    date_issued    = models.DateField()
    image          = models.ImageField(upload_to='certificates/')
    credential_url = models.URLField(blank=True)

    class Meta:
        ordering = ['-date_issued']

    def __str__(self):
        return f"{self.title} - {self.issuer}"


class Skill(models.Model):
    CATEGORY = [
        ('frontend', 'Frontend'),
        ('backend',  'Backend'),
        ('tool',     'Tools & DevOps'),
        ('design',   'UI/UX Design'),
    ]
    name        = models.CharField(max_length=100)
    category    = models.CharField(max_length=20, choices=CATEGORY)
    proficiency = models.IntegerField(default=80, help_text="Persentase kemahiran (0-100)")
    icon_class  = models.CharField(max_length=100, blank=True, help_text="Class icon FontAwesome. Contoh: fab fa-python, fab fa-js-square")
    order       = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class WorkExperience(models.Model):
    company     = models.CharField(max_length=200)
    role        = models.CharField(max_length=200)
    description = models.TextField()
    start_date  = models.DateField()
    end_date    = models.DateField(null=True, blank=True, help_text="Kosongkan jika masih aktif bekerja")

    @property
    def is_current(self):
        return self.end_date is None

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.role} di {self.company}"


class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree      = models.CharField(max_length=200, help_text="Contoh: Sarjana Komputer (S.Kom)")
    field       = models.CharField(max_length=200, help_text="Contoh: Teknik Informatika")
    year_start  = models.IntegerField()
    year_end    = models.IntegerField(null=True, blank=True, help_text="Kosongkan jika masih menempuh studi")

    class Meta:
        ordering = ['-year_start']

    def __str__(self):
        return f"{self.degree} - {self.institution}"

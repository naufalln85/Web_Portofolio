import os
import shutil
from datetime import date
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from portfolio.models import Profile, Project, Certificate, Skill, WorkExperience, Education


class Command(BaseCommand):
    help = 'Mempopulasikan database dengan profil, keahlian, sertifikat, dan proyek Naufal Maulana Hasan'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Memulai proses seeding data Naufal Maulana Hasan...')

        # =====================================================================
        # 1. SETUP MEDIA DIRECTORIES
        # =====================================================================
        media_root = settings.MEDIA_ROOT
        profile_media_dir = os.path.join(media_root, 'profile')
        projects_media_dir = os.path.join(media_root, 'projects')
        certs_media_dir = os.path.join(media_root, 'certificates')
        cv_media_dir = os.path.join(media_root, 'cv')

        for d in [profile_media_dir, projects_media_dir, certs_media_dir, cv_media_dir]:
            os.makedirs(d, exist_ok=True)

        # =====================================================================
        # 2. COPY USER'S REAL IMAGES FROM aset_cv/images/ TO media/
        # =====================================================================
        images_src_dir = os.path.join(settings.BASE_DIR, 'portfolio', 'aset_cv', 'images')

        image_mappings = [
            # (source filename in aset_cv/images/, destination path in media/)
            ('profile.jpg', os.path.join(profile_media_dir, 'avatar.jpg')),
            ('smart_parking.jpg', os.path.join(projects_media_dir, 'smart_parking.jpg')),
            ('k8s_monitoring.jpg', os.path.join(projects_media_dir, 'k8s_monitoring.jpg')),
            ('smart_agriculture.jpg', os.path.join(projects_media_dir, 'smart_agriculture.jpg')),
            ('cert_nde.jpg', os.path.join(certs_media_dir, 'cert_nde.jpg')),
            ('cert_2.jpg', os.path.join(certs_media_dir, 'cert_2.jpg')),
            ('cert_3.jpg', os.path.join(certs_media_dir, 'cert_3.jpg')),
        ]

        for src_name, dest_path in image_mappings:
            src_path = os.path.join(images_src_dir, src_name)
            if os.path.exists(src_path):
                shutil.copy2(src_path, dest_path)
                self.stdout.write(f'  ✓ Menyalin {src_name} → {os.path.basename(dest_path)}')
            else:
                self.stdout.write(self.style.WARNING(
                    f'  ⚠️  {src_name} belum ada di portfolio/aset_cv/images/. '
                    f'Silakan simpan file gambar di sana lalu jalankan ulang.'
                ))

        # =====================================================================
        # 3. COPY ORIGINAL CV PDF
        # =====================================================================
        cv_source = os.path.join(settings.BASE_DIR, 'portfolio', 'aset_cv',
                                 'CV_Naufal Maulana Hasan_103032500156.pdf')
        cv_dest = os.path.join(cv_media_dir, 'CV_Naufal_Maulana_Hasan.pdf')
        if os.path.exists(cv_source):
            shutil.copy2(cv_source, cv_dest)
            self.stdout.write('  ✓ File CV asli berhasil disalin ke media/cv/')
        else:
            self.stdout.write(self.style.WARNING('  ⚠️  File CV asli tidak ditemukan!'))

        # =====================================================================
        # 4. CLEAR OLD DATA
        # =====================================================================
        self.stdout.write('🧹 Membersihkan database dari data lama...')
        Profile.objects.all().delete()
        Project.objects.all().delete()
        Certificate.objects.all().delete()
        Skill.objects.all().delete()
        WorkExperience.objects.all().delete()
        Education.objects.all().delete()

        # =====================================================================
        # 5. SEED PROFILE
        # =====================================================================
        self.stdout.write('👤 Membuat profil Naufal...')
        Profile.objects.create(
            name='Naufal Maulana Hasan',
            title='DevOps Specialist & Cloud Engineer',
            tagline=(
                'DevOps Specialist & Cloud Engineer dengan hasrat tinggi dalam '
                'otomatisasi infrastruktur, orkestrasi cloud, dan keamanan jaringan.'
            ),
            bio=(
                'Saya Naufal Maulana Hasan, mahasiswa Teknik Informatika di Universitas Telkom '
                'dan alumni SMK Telkom Sandy Putra Purwokerto jurusan Teknik Komputer Jaringan. '
                'Memiliki minat berkarir sebagai IT Support (DevOps spesialis atau Cloud Engineer) '
                'serta mahir dalam business process, compliance, dan internal control. '
                'Seorang lifelong learner yang sangat familiar dengan ekosistem Linux, GitHub, '
                'dan GitLab. Berpengalaman mengembangkan proyek IoT berbasis NodeMCU dan ESP32, '
                'serta membangun sistem monitoring infrastruktur Kubernetes menggunakan Prometheus '
                'dan Grafana. Aktif berorganisasi sebagai Ketua Panitia BMTS dan koordinator acara '
                'di AKABARA 30.'
            ),
            email='naufalmaulanahasan@gmail.com',
            github_url='https://github.com/naufalln85',
            linkedin_url='https://linkedin.com/in/naufalmaulanahasan',
            photo='profile/avatar.jpg',
            cv_file='cv/CV_Naufal_Maulana_Hasan.pdf',
            accent_color='#00C978',
        )

        # =====================================================================
        # 6. SEED SKILLS  (Cloud, DevOps, Network → ~80%)
        # =====================================================================
        self.stdout.write('🛠️  Membuat data keahlian (Skills)...')
        skills_data = [
            # ── DevOps & Tools ──
            {'name': 'DevOps (CI/CD Pipeline)',       'category': 'devops',   'proficiency': 80, 'icon_class': 'fa-solid fa-infinity',        'order': 1},
            {'name': 'Linux System Administration',   'category': 'devops',   'proficiency': 85, 'icon_class': 'fa-brands fa-linux',           'order': 2},
            {'name': 'Docker & Kubernetes',           'category': 'devops',   'proficiency': 85, 'icon_class': 'fa-brands fa-docker',          'order': 3},
            {'name': 'Git & GitHub / GitLab CI-CD',   'category': 'devops',   'proficiency': 80, 'icon_class': 'fa-brands fa-git-alt',         'order': 4},
            {'name': 'Prometheus & Grafana',          'category': 'devops',   'proficiency': 80, 'icon_class': 'fa-solid fa-chart-line',       'order': 5},
            {'name': 'ELK Stack (Elasticsearch)',     'category': 'devops',   'proficiency': 75, 'icon_class': 'fa-solid fa-magnifying-glass-chart', 'order': 6},
            # ── Cloud Computing ──
            {'name': 'OpenStack Cloud',               'category': 'cloud',    'proficiency': 80, 'icon_class': 'fa-solid fa-cloud',            'order': 1},
            {'name': 'Server Administration',         'category': 'cloud',    'proficiency': 80, 'icon_class': 'fa-solid fa-server',           'order': 2},
            # ── Networking ──
            {'name': 'Cisco Networking (Routing/Switching)', 'category': 'network', 'proficiency': 80, 'icon_class': 'fa-solid fa-network-wired', 'order': 1},
            {'name': 'Network Security',              'category': 'network',  'proficiency': 80, 'icon_class': 'fa-solid fa-shield-halved',    'order': 2},
            # ── Backend / IoT ──
            {'name': 'Internet of Things (IoT)',      'category': 'backend',  'proficiency': 75, 'icon_class': 'fa-solid fa-microchip',        'order': 1},
            {'name': 'Python & Flask',                'category': 'backend',  'proficiency': 70, 'icon_class': 'fa-brands fa-python',          'order': 2},
        ]
        for s in skills_data:
            Skill.objects.create(**s)

        # =====================================================================
        # 7. SEED 3 PROJECTS
        # =====================================================================
        self.stdout.write('📂 Membuat data proyek (Projects)...')

        Project.objects.create(
            title='Smart Parking IoT System',
            category='iot',
            description=(
                'Proyek Smart Parking IoT untuk mengatasi keterbatasan ruang parkir. '
                'Menggunakan NodeMCU ESP32 + sensor ultrasonik HC-SR04, LED indikator, '
                'dan buzzer untuk mendeteksi status slot (kosong/terisi/booking). '
                'Data dikirim real-time via MQTT ke ThingsBoard Cloud Platform. '
                'Backend dibangun dengan Python Flask API yang menyajikan web dashboard '
                'interaktif untuk pemantauan langsung, dilengkapi sistem alarm buzzer '
                'jika terjadi pelanggaran slot booking.'
            ),
            tech_stack='NodeMCU ESP32, HC-SR04, MQTT, ThingsBoard, Python, Flask, HTML/CSS/JS, WireGuard',
            thumbnail='projects/smart_parking.jpg',
            repo_url='https://github.com/naufalln85/smart-parking-iot',
            order=1,
            is_featured=True,
        )

        Project.objects.create(
            title='Kubernetes Monitoring with Prometheus & Grafana',
            category='devops',
            description=(
                'Implementasi monitoring klaster Kubernetes (v1.28.15) menggunakan Prometheus '
                'dan Grafana. Klaster 3 VM Ubuntu (master + worker + monitoring). '
                'DaemonSet Node Exporter untuk metrik fisik (CPU, RAM, Disk), Kube State Metrics '
                'untuk status objek K8s API, dan Metrics Server untuk HPA. '
                'Service diekspos via MetalLB LoadBalancer (IP Pool 10.1.1.100-110). '
                'Alertmanager dengan email notification untuk notifikasi memory pressure & pod crash.'
            ),
            tech_stack='Kubernetes, Kubeadm, Prometheus, Grafana, Node Exporter, Kube State Metrics, MetalLB, Alertmanager, Flannel CNI',
            thumbnail='projects/k8s_monitoring.jpg',
            repo_url='https://github.com/naufalln85/k8s-monitoring-prometheus-grafana',
            order=2,
            is_featured=True,
        )

        Project.objects.create(
            title='Smart Agricultural Water Level Monitoring',
            category='iot',
            description=(
                'Sistem mitigasi banjir sawah otomatis berbasis IoT untuk mencegah gagal panen '
                'akibat cuaca ekstrem. NodeMCU ESP8266 mengintegrasikan Water Level Sensor, '
                'Raindrop Sensor YL-83, dan DHT11 (suhu & kelembaban). Data dikirim ke Blynk IoT '
                'Cloud untuk pemantauan via smartphone. Alarm lokal: buzzer aktif + LED multi-warna '
                '(Hijau = Aman, Kuning = Waspada Hujan, Merah = Bahaya Banjir).'
            ),
            tech_stack='NodeMCU ESP8266, YL-83, Water Level Sensor, DHT11, Blynk IoT Cloud, Arduino IDE, C++',
            thumbnail='projects/smart_agriculture.jpg',
            repo_url='https://github.com/naufalln85/smart-agricultural-water-level',
            order=3,
            is_featured=True,
        )

        # =====================================================================
        # 8. SEED 3 CERTIFICATES (hanya 3 sesuai permintaan)
        # =====================================================================
        self.stdout.write('📜 Membuat data sertifikasi (3 sertifikat)...')

        Certificate.objects.create(
            title='Network Defense Essentials (NDE)',
            issuer='EC-Council',
            date_issued=date(2025, 5, 14),
            image='certificates/cert_nde.jpg',
        )
        Certificate.objects.create(
            title='Kubernetes Cluster Administration',
            issuer='Btech Academy (ADINUSA)',
            date_issued=date(2025, 3, 10),
            image='certificates/cert_2.jpg',
        )
        Certificate.objects.create(
            title='Networking Essentials',
            issuer='Cisco Networking Academy',
            date_issued=date(2023, 11, 27),
            image='certificates/cert_3.jpg',
        )

        # =====================================================================
        # 9. SEED WORK EXPERIENCE
        # =====================================================================
        self.stdout.write('💼 Membuat data pengalaman...')

        WorkExperience.objects.create(
            company='Akademi Digital Nusantara (ADINUSA) – PT Boer Technology',
            role='DevOps & Cloud Intern',
            start_date=date(2024, 6, 1),
            end_date=date(2024, 11, 30),
            description=(
                '• Pengujian & validasi kurikulum course DevOps: GitHub Actions CI/CD, '
                'Jenkins dengan GitLab CI/CD, dan keamanan sistem Linux.\n'
                '• Simulasi monitoring infrastruktur menggunakan klaster Kubernetes terdistribusi.\n'
                '• Publikasi analisis monitoring Kubernetes dengan Prometheus & Grafana pada blog publik.'
            ),
        )
        WorkExperience.objects.create(
            company='SMK Telkom Sandy Putra Purwokerto',
            role='Siswa / IoT Project Developer',
            start_date=date(2022, 6, 1),
            end_date=date(2025, 6, 1),
            description=(
                '• Mengembangkan proyek Smart Parking berbasis IoT + web dashboard.\n'
                '• Ketua Panitia Bakti Masyarakat Telkom School (BMTS) dan Koordinator Acara AKABARA 30.\n'
                '• Master of Ceremony (MC) berbagai kegiatan internal & eksternal sekolah.\n'
                '• Meraih sertifikasi kompetensi industri bidang jaringan & keamanan sistem.'
            ),
        )

        # =====================================================================
        # 10. SEED EDUCATION
        # =====================================================================
        self.stdout.write('🎓 Membuat data pendidikan...')

        Education.objects.create(
            institution='Universitas Telkom',
            degree='Sarjana Komputer (S.Kom) – Sedang Menempuh',
            field='Teknik Informatika / Ilmu Komputer',
            year_start=2025,
            year_end=None,
        )
        Education.objects.create(
            institution='SMK Telkom Sandy Putra Purwokerto',
            degree='Sekolah Menengah Kejuruan (SMK)',
            field='Teknik Komputer Jaringan (TKJ)',
            year_start=2022,
            year_end=2025,
        )

        # =====================================================================
        # 11. CREATE ADMIN SUPERUSER
        # =====================================================================
        self.stdout.write('🔑 Membuat akun superuser...')
        if not User.objects.filter(username='naufal').exists():
            User.objects.create_superuser('naufal', 'naufalmaulanahasan@gmail.com', 'Naufal123!')
            self.stdout.write("  ✓ Akun superuser 'naufal' dibuat (password: Naufal123!)")
        else:
            self.stdout.write("  ✓ Akun 'naufal' sudah ada, melewati.")

        self.stdout.write(self.style.SUCCESS(
            '\n✨ Seeding portfolio Naufal Maulana Hasan BERHASIL!\n'
            'Jalankan: python manage.py runserver'
        ))

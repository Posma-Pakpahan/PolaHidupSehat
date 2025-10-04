# 🎯 Pola Hidup Tracker

[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Aplikasi web profesional untuk melacak dan memantau pola hidup sehat dengan sistem authentication, template berbasis penelitian, dan deployment-ready untuk VPS.**

## 🌟 **Live Demo**
- **Website**: [tracker.posma-pakpahan.me](https://tracker.posma-pakpahan.me)
- **Admin Panel**: [tracker.posma-pakpahan.me/admin](https://tracker.posma-pakpahan.me/admin)

## ✨ **Fitur Unggulan**

### 🔐 **Multi-User Authentication**
- **User Management**: Login, register, logout dengan validasi lengkap
- **User Profiles**: Extended user data dengan avatar, timezone, statistics
- **Security**: Login required untuk semua tracking operations
- **Admin Interface**: Full control via Django admin panel

### 📅 **Template Pola Hidup Sehat**
- **SENIN** (Fresh Start): Bangun 05:30, baca Alkitab, olahraga, belajar 2 jam, tugas
- **SELASA** (Kuliah Penuh): Bangun 05:00, kuliah 07:30-15:30, review materi, belajar malam
- **RABU** (Recovery): Bangun 05:30, skill development, proyek personal, sosialisasi
- **KAMIS** (Kuliah): Bangun 05:00, kuliah 07:30-12:00, belajar fokus, persiapan weekend
- **JUMAT** (Produktif): Bangun 05:30, belajar intensif, selesaikan tugas, cleaning
- **SABTU** (Pelayanan): Bangun 06:00, latihan ibadah Naposo, fellowship, rekreasi
- **MINGGU** (Ibadah & Rest): Bangun 06:00, ibadah gereja, family time, tugas mingguan

### 🕐 **Jadwal Harian Berdasarkan Penelitian Kesehatan**
- **05:00-06:00**: Bangun pagi, doa syukur, baca Alkitab 5-20 menit
- **06:00-07:00**: Olahraga pagi, persiapan, mandi
- **07:00-08:00**: Sarapan sehat, persiapan aktivitas
- **08:00-12:00**: Waktu produktif utama (kuliah/belajar/tugas)
- **12:00-13:30**: Makan siang, istirahat/power nap
- **13:30-17:00**: Aktivitas sore (belajar/proyek/skill development)
- **17:00-18:30**: Olahraga sore, relaksasi, sosialisasi
- **18:30-19:30**: Makan malam keluarga
- **19:30-21:30**: Quality time, belajar ringan, persiapan besok
- **21:30-22:00**: Doa malam, refleksi, gratitude
- **22:00-22:30**: Tidur (7-8 jam untuk kesehatan optimal)

### 📊 **Progress Tracking & Analytics**
- Persentase penyelesaian real-time dengan progress bars
- Visual statistics dengan completion rate per minggu
- Achievement system dengan milestone tracking
- User statistics: total weeks, activities, streaks
- Weekly navigation untuk melihat progress historis

### 🎨 **Design Professional**
- Bootstrap 5 dengan custom styling dan gradient backgrounds
- Responsive design untuk desktop dan mobile
- Smooth animations dan hover effects
- Modern card-based layout dengan consistent spacing
- Dark mode friendly design elements

## 🛠️ **Tech Stack**

- **Backend**: Django 5.2.7 dengan authentication system
- **Frontend**: Bootstrap 5.3.2 + Custom CSS + jQuery AJAX
- **Database**: SQLite (development) / PostgreSQL (production)
- **Deployment**: Gunicorn + Nginx + SystemD
- **Caching**: Redis untuk session dan cache management
- **Icons**: Bootstrap Icons untuk UI elements

## 🚀 **Quick Start - Development**

### 1. **Clone Repository**
```bash
git clone https://github.com/posma-pakpahan/pola-hidup-tracker.git
cd pola-hidup-tracker
```

### 2. **Setup Virtual Environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Environment Configuration**
```bash
cp .env.example .env
# Edit .env file dengan konfigurasi Anda
```

### 5. **Database Setup**
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. **Apply Healthy Lifestyle Template**
```bash
# Untuk user tertentu
python manage.py apply_healthy_template --user your_username --current-week-only

# Untuk semua user
python manage.py apply_healthy_template
```

### 7. **Run Development Server**
```bash
python manage.py runserver
```

**Buka: `http://127.0.0.1:8000/`**

## 🚀 **Production Deployment (VPS)**

### 📋 **Pre-requisites**
- VPS Ubuntu 20.04+ dengan minimum 1GB RAM
- Domain pointing ke VPS IP
- SSH access ke VPS

### 🔧 **Automated Deployment**
```bash
# Connect to VPS
ssh root@your-vps-ip

# Run deployment script
wget https://raw.githubusercontent.com/posma-pakpahan/pola-hidup-tracker/main/deploy.sh
chmod +x deploy.sh
./deploy.sh
```

### ⚙️ **Manual Deployment Steps**

#### 1. **System Setup**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.11 python3.11-venv python3-pip nginx postgresql redis-server git
```

#### 2. **Project Setup**
```bash
sudo mkdir -p /var/www/pola_hidup_tracker
sudo chown $USER:$USER /var/www/pola_hidup_tracker
git clone https://github.com/posma-pakpahan/pola-hidup-tracker.git /var/www/pola_hidup_tracker
cd /var/www/pola_hidup_tracker
```

#### 3. **Python Environment**
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 4. **Database Setup**
```bash
sudo -u postgres createdb pola_hidup_tracker
sudo -u postgres createuser tracker_user
# Set password in PostgreSQL console
```

#### 5. **Django Configuration**
```bash
cp .env.example .env
# Edit .env dengan konfigurasi production
python manage.py migrate --settings=pola_hidup_tracker.production_settings
python manage.py createsuperuser --settings=pola_hidup_tracker.production_settings
python manage.py collectstatic --noinput --settings=pola_hidup_tracker.production_settings
```

#### 6. **Apply Template**
```bash
python manage.py apply_healthy_template --user admin --current-week-only --settings=pola_hidup_tracker.production_settings
```

#### 7. **Service Configuration**

**Gunicorn Service (`/etc/systemd/system/pola-hidup-tracker.service`):**
```ini
[Unit]
Description=Pola Hidup Tracker Django application
After=network.target

[Service]
User=your_user
Group=www-data
WorkingDirectory=/var/www/pola_hidup_tracker
Environment="PATH=/var/www/pola_hidup_tracker/venv/bin"
ExecStart=/var/www/pola_hidup_tracker/venv/bin/gunicorn --workers 3 --bind unix:/var/www/pola_hidup_tracker/pola_hidup_tracker.sock pola_hidup_tracker.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

**Nginx Configuration (`/etc/nginx/sites-available/pola-hidup-tracker`):**
```nginx
server {
    listen 80;
    server_name your-domain.com your-vps-ip;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/pola_hidup_tracker/staticfiles/;
        expires 30d;
    }
    
    location /media/ {
        alias /var/www/pola_hidup_tracker/mediafiles/;
        expires 30d;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/pola_hidup_tracker/pola_hidup_tracker.sock;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 8. **Enable Services**
```bash
sudo systemctl daemon-reload
sudo systemctl start pola-hidup-tracker
sudo systemctl enable pola-hidup-tracker
sudo ln -s /etc/nginx/sites-available/pola-hidup-tracker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 9. **SSL Setup (Optional)**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 🔄 **Updates & Maintenance**

### **Update Application**
```bash
cd /var/www/pola_hidup_tracker
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --settings=pola_hidup_tracker.production_settings
python manage.py collectstatic --noinput --settings=pola_hidup_tracker.production_settings
sudo systemctl restart pola-hidup-tracker
```

### **Monitoring**
```bash
# Check application status
sudo systemctl status pola-hidup-tracker

# View logs
sudo journalctl -u pola-hidup-tracker -f
tail -f /var/www/pola_hidup_tracker/logs/django.log

# Check Nginx
sudo systemctl status nginx
sudo tail -f /var/log/nginx/error.log
```

## 📁 **Project Structure**

```
pola-hidup-tracker/
├── manage.py
├── requirements.txt
├── .gitignore
├── .env.example
├── deploy.sh                       # 🚀 Deployment script
├── update.sh                       # 🔄 Update script
├── gunicorn_start.sh              # ⚙️ Gunicorn starter
├── db.sqlite3                     # 🗄️ Development database
├── logs/                          # 📋 Application logs
├── pola_hidup_tracker/            # 🏗️ Project settings
│   ├── settings.py                # Development settings
│   ├── production_settings.py     # Production settings
│   ├── urls.py
│   └── wsgi.py
├── tracker/                       # 📱 Main application
│   ├── models.py                  # Week, Activity, UserProfile
│   ├── views.py                   # Business logic
│   ├── auth_forms.py              # Authentication forms
│   ├── forms.py                   # Activity forms
│   ├── urls.py                    # URL routing
│   ├── admin.py                   # Admin interface
│   ├── migrations/                # Database migrations
│   ├── management/commands/       # Custom commands
│   │   └── apply_healthy_template.py
│   └── templatetags/              # Custom template filters
├── templates/                     # 🎨 HTML templates
│   ├── base.html                  # Base template
│   ├── tracker/                   # Main app templates
│   │   ├── home.html              # Landing page
│   │   ├── dashboard.html         # Main tracker
│   │   ├── profile.html           # User profile
│   │   ├── stats.html             # Statistics
│   │   ├── add_activity.html
│   │   ├── edit_activity.html
│   │   └── delete_activity.html
│   └── registration/              # Auth templates
│       ├── login.html
│       └── register.html
└── static/                        # 🎨 Static files
```

## 💻 **Usage Guide**

### **📊 Dashboard Features**
1. **Week Navigation**: Klik panah untuk lihat minggu lain
2. **Progress Bar**: Otomatis update saat aktivitas di-check
3. **Add Activity**: Klik tombol + pada card hari yang diinginkan
4. **Toggle Complete**: Klik checkbox untuk mark as done
5. **Edit/Delete**: Menu 3 dots pada aktivitas (kecuali default)

### **📈 User Management**
- **Registration**: Users dapat mendaftar sendiri
- **Profile**: Update nama, timezone, avatar
- **Statistics**: Personal completion rate, streaks, achievements

### **⚙️ Admin Panel**
- **Access**: `/admin/` dengan superuser credentials
- **User Management**: Kelola users dan permissions
- **Data Management**: Monitor activities dan weeks
- **Template Application**: Apply templates untuk users

## 🎨 **Customization**

### **Template Modification**
Edit `tracker/models.py` method `create_default_activities()`:
```python
default_activities = [
    {'day': 'senin', 'name': 'Custom Activity', 'time': '06:00-07:00', 'is_default': True},
    # Add your custom activities
]
```

### **Styling**
Edit `templates/base.html` CSS section:
```css
/* Custom theme colors */
.navbar-custom {
    background: linear-gradient(135deg, #your-color1 0%, #your-color2 100%);
}
```

### **Environment Variables**
```bash
# .env file
DEBUG=False
SECRET_KEY=your-secret-key
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
ALLOWED_HOSTS=your-domain.com,your-ip
```

## 🏆 **Features Showcase**

### **📱 Responsive Design**
- Mobile-first approach dengan Bootstrap 5
- Touch-friendly interface untuk mobile users
- Consistent experience di semua device sizes

### **🎯 Achievement System**
- **First Week**: Menyelesaikan minggu pertama
- **High Achiever**: Completion rate di atas 80%
- **Week Warrior**: Konsisten selama seminggu
- **Century Club**: Lebih dari 100 aktivitas

### **📊 Analytics & Statistics**
- Personal completion rate tracking
- Weekly progress visualization
- Activity completion trends
- User engagement metrics

## 🤝 **Contributing**

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Django Framework** untuk robust backend development
- **Bootstrap 5** untuk responsive UI components
- **Research-based** healthy lifestyle patterns
- **Indonesian Christian** spiritual activities integration

## 📞 **Support**

- **Issues**: [GitHub Issues](https://github.com/posma-pakpahan/pola-hidup-tracker/issues)
- **Documentation**: [Project Wiki](https://github.com/posma-pakpahan/pola-hidup-tracker/wiki)
- **Email**: admin@posma-pakpahan.me

---

**Dibuat dengan ❤️ untuk mendukung pola hidup sehat dan spiritual yang seimbang**

**🚀 Ready for Production | 📱 Mobile-Friendly | 🔒 Secure | ⚡ Fast**
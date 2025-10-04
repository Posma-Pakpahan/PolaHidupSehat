# 🎯 Pola Hidup Tracker - Personal Edition (No Login)

Aplikasi web personal untuk melacak dan ## 🚀 Production Deployment (VPS)

### 📋 **Pre-requisites**
- VPS Ubuntu 20.04+ dengan minimum 1GB RAM
- Domain pointing ke VPS IP (tracker.posma-pakpahan.me → 31.97.221.115)
- SSH access ke VPS

### 🔧 **Deployment Steps**

#### 1. **Connect to VPS**
```bash
ssh root@31.97.221.115
# atau 
ssh your_user@tracker.posma-pakpahan.me
```

#### 2. **Run Deployment Script**
```bash
# Upload dan jalankan script deployment
wget https://raw.githubusercontent.com/your-repo/deploy.sh
chmod +x deploy.sh
./deploy.sh
```

#### 3. **Manual Deployment (Alternative)**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.11 python3.11-venv python3-pip nginx postgresql redis-server git

# Clone project
sudo mkdir -p /var/www/pola_hidup_tracker
sudo chown $USER:$USER /var/www/pola_hidup_tracker
git clone https://github.com/your-repo.git /var/www/pola_hidup_tracker

# Setup virtual environment
cd /var/www/pola_hidup_tracker
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup database
sudo -u postgres createdb pola_hidup_tracker
sudo -u postgres createuser tracker_user
# Set password in PostgreSQL

# Run migrations
python manage.py migrate --settings=pola_hidup_tracker.production_settings

# Create superuser
python manage.py createsuperuser --settings=pola_hidup_tracker.production_settings

# Apply template
python manage.py apply_healthy_template --user admin --current-week-only --settings=pola_hidup_tracker.production_settings

# Collect static files
python manage.py collectstatic --noinput --settings=pola_hidup_tracker.production_settings
```

#### 4. **Configure Services**

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
    server_name tracker.posma-pakpahan.me 31.97.221.115;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/pola_hidup_tracker/staticfiles/;
    }
    
    location /media/ {
        alias /var/www/pola_hidup_tracker/mediafiles/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/pola_hidup_tracker/pola_hidup_tracker.sock;
    }
}
```

#### 5. **Enable Services**
```bash
sudo systemctl daemon-reload
sudo systemctl start pola-hidup-tracker
sudo systemctl enable pola-hidup-tracker
sudo ln -s /etc/nginx/sites-available/pola-hidup-tracker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 6. **SSL Setup (Optional)**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tracker.posma-pakpahan.me
```

### 🔄 **Updates**
```bash
cd /var/www/pola_hidup_tracker
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --settings=pola_hidup_tracker.production_settings
python manage.py collectstatic --noinput --settings=pola_hidup_tracker.production_settings
sudo systemctl restart pola-hidup-tracker
```

### 📊 **Monitoring**
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

### 🎯 **Post-Deployment**
1. **Access Application**: `https://tracker.posma-pakpahan.me`
2. **Admin Panel**: `https://tracker.posma-pakpahan.me/admin/`
3. **Create Users**: Register via web interface atau admin panel
4. **Apply Templates**: Gunakan management command untuk user baru

### 🔧 **Environment Variables (.env)**
```bash
DEBUG=False
SECRET_KEY=your-secret-key
DB_NAME=pola_hidup_tracker
DB_USER=tracker_user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
USE_HTTPS=True
```emantau pola hidup sehat tanpa sistem login. Khusus untuk penggunaan pribadi dengan desain modern menggunakan Django dan Bootstrap 5.

## ✨ Fitur Unggulan

### 🏠 **Dashboard Personal**
- **No Login Required**: Langsung bisa digunakan!
- Navigasi mingguan yang mudah (minggu lalu, sekarang, depan)
- Progress bar real-time untuk tracking mingguan
- Layout responsif untuk desktop dan mobile
- Animasi smooth dan hover effects

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

### 📊 **Progress Tracking & Statistics**
- Persentase penyelesaian real-time
- Visual progress bar dengan gradient colors
- Halaman statistik lengkap dengan achievement system
- Total aktivitas, completion rate, dan pencapaian

### �️ **Database SQLite**
- **File Local**: `db.sqlite3` - ringan dan portable
- **No Server Required**: Tidak perlu instalasi database terpisah
- **Easy Backup**: Cukup copy file database
- **Admin Interface**: Kelola data via Django admin

### 🎨 **Design Professional**
- Bootstrap 5 dengan custom styling
- Gradient backgrounds dan modern cards
- Inter font untuk readability optimal
- Consistent color scheme dan spacing
- Mobile-first responsive design

## 🛠️ Teknologi

- **Backend**: Django 5.2.7 (No Auth System)
- **Frontend**: Bootstrap 5.3.2 + Custom CSS
- **Database**: SQLite (Personal Use)
- **Icons**: Bootstrap Icons
- **JavaScript**: jQuery untuk AJAX
- **Python**: 3.13+

## � Quick Start

### 1. **Setup & Install**
```bash
cd Pola_Hidup_Tracker
pip install Django>=5.2 Pillow python-dateutil whitenoise
```

### 2. **Database Setup**
```bash
python manage.py migrate
python manage.py createsuperuser  # Optional, untuk admin
```

### 3. **Apply Healthy Lifestyle Template**
```bash
# Untuk minggu ini saja (recommended untuk start)
python manage.py apply_healthy_template --current-week-only

# Untuk semua minggu (jika sudah ada data sebelumnya)
python manage.py apply_healthy_template
```

### 4. **Run Server**
```bash
python manage.py runserver
```

### 5. **Access App**
```
URL: http://127.0.0.1:8000/
Langsung masuk Dashboard dengan 106 aktivitas template! 🎉
```

## �📁 Struktur Project (Simplified)

```
Pola_Hidup_Tracker/
├── manage.py
├── db.sqlite3                      # 🗄️ Database file (backup ini!)
├── requirements.txt
├── DATABASE_GUIDE.md               # 📖 Panduan database lengkap
├── pola_hidup_tracker/             # Project settings
├── tracker/                        # Main app (no auth)
│   ├── models.py                   # Week, Activity models only
│   ├── views.py                    # No login_required decorators
│   ├── forms.py                    # Activity form
│   ├── urls.py                     # Simplified routing
│   └── admin.py                    # Admin interface
├── templates/                      # Clean templates
│   ├── base.html                   # Navbar tanpa login/logout
│   ├── tracker/
│   │   ├── dashboard.html          # Main interface
│   │   ├── stats.html              # Statistics page
│   │   ├── add_activity.html
│   │   ├── edit_activity.html
│   │   └── delete_activity.html
└── static/                         # Static files
```

## � Cara Penggunaan

### **📊 Dashboard Features**
1. **Week Navigation**: Klik panah untuk lihat minggu lain
2. **Progress Bar**: Otomatis update saat aktivitas di-check
3. **Add Activity**: Klik tombol + pada card hari yang diinginkan
4. **Toggle Complete**: Klik checkbox untuk mark as done
5. **Edit/Delete**: Menu 3 dots pada aktivitas (kecuali default)

### **📈 Statistics Page**
- Akses: `http://127.0.0.1:8000/stats/`
- Total minggu, aktivitas, completion rate
- Achievement badges berdasarkan performa
- Info database dan backup guide

### **⚙️ Admin Panel**
- Akses: `http://127.0.0.1:8000/admin/`
- Kelola data Week dan Activity
- Monitor penggunaan aplikasi

## 🗄️ Database Management

### **🔄 Backup Data**
```bash
# Simple backup
copy db.sqlite3 backup_2025-10-04.sqlite3

# JSON export
python manage.py dumpdata tracker > backup.json
```

### **📥 Restore Data**
```bash
# Simple restore
copy backup_2025-10-04.sqlite3 db.sqlite3

# JSON import
python manage.py loaddata backup.json
```

### **🗑️ Reset Data**
```bash
del db.sqlite3
python manage.py migrate
```

## 🎨 Customization

### **Ubah Default Activities**
Edit `tracker/models.py`:
```python
default_activities = [
    {'day': 'senin', 'name': 'Olahraga', 'time': '06:00-07:00', 'is_default': True},
    # Tambah/edit sesuai kebutuhan
]
```

### **Ubah Theme Colors**
Edit `templates/base.html`:
```css
/* Primary gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Progress bar */
background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
```

## 🔧 Technical Details

### **Simplified Architecture**
- ❌ **Removed**: User authentication, profiles, multi-user support
- ✅ **Kept**: All core features, AJAX, responsive design, admin
- 🚀 **Benefit**: Faster, simpler, perfect for personal use

### **Database Schema**
```sql
tracker_week:           # Mingguan data
- id, start_date (unique), end_date, timestamps

tracker_activity:       # Aktivitas harian  
- id, week_id, day, name, time, completed, is_default, timestamps
```

### **Performance**
- Lightweight SQLite database
- Efficient queries without user filtering
- AJAX for smooth interactions
- Minimal external dependencies

## 🎯 Keunggulan Personal Edition

1. **🚀 Zero Setup Auth**: No registration, no login hassle
2. **� Portable Database**: Single SQLite file, easy backup
3. **🔒 Privacy**: No user data, no external connections
4. **⚡ Fast**: No auth overhead, direct access
5. **🎛️ Full Control**: Complete admin access to your data
6. **📱 Responsive**: Perfect di desktop dan mobile
7. **🎨 Professional**: Modern UI dengan Bootstrap 5

## 🆘 Troubleshooting

### **Common Issues**
```bash
# Port sudah digunakan?
python manage.py runserver 8001

# Database corrupt?
del db.sqlite3 && python manage.py migrate

# Performance lambat?
python manage.py flush  # Reset semua data
```

## 📊 File Sizes
- **App Size**: ~2 MB
- **Database**: 1-5 MB per tahun
- **Backup**: Same as database size

## 🔄 Migration dari Multi-User

Jika Anda punya data dari versi multi-user sebelumnya:
```bash
# Data akan dimigrate otomatis
python manage.py migrate
# User references akan dihapus, data activities tetap ada
```

---

## � **Ready to Use!**

**Aplikasi Pola Hidup Tracker Personal Edition** siap digunakan dengan semua fitur lengkap tanpa kerumitan sistem login!

### **🚀 Start Tracking:**
```bash
python manage.py runserver
# Buka: http://127.0.0.1:8000/
# Langsung bisa digunakan! 🎯
```

### **� More Info:**
- Baca `DATABASE_GUIDE.md` untuk panduan database lengkap
- Check `templates/tracker/stats.html` untuk info database di app

---

**Dibuat dengan ❤️ menggunakan Django + Bootstrap 5 untuk penggunaan personal**

**Happy Tracking! 📅✨**
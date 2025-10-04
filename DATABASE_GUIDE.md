# 📖 Database & Aplikasi Pola Hidup Tracker - Personal Edition

## 🗄️ **Database SQLite - Panduan Lengkap**

### **Apa itu SQLite?**
SQLite adalah database engine yang sangat ringan dan tidak memerlukan server terpisah. Perfect untuk penggunaan personal!

### **📁 Lokasi Database**
```
Pola_Hidup_Tracker/
└── db.sqlite3          <- File database Anda ada di sini!
```

### **🔧 Struktur Database**

#### **Tabel: `tracker_week`**
Menyimpan data mingguan:
```sql
- id (Primary Key)
- start_date (Tanggal Senin)  
- end_date (Tanggal Minggu)
- created_at
- updated_at
```

#### **Tabel: `tracker_activity`**
Menyimpan aktivitas harian:
```sql
- id (Primary Key)
- week_id (Foreign Key ke Week)
- day (senin/selasa/rabu/dst)
- name (Nama aktivitas)
- time (Waktu, optional)
- completed (True/False)
- is_default (True untuk jadwal tetap)
- created_at
- updated_at
```

### **💾 Backup & Restore Data**

#### **Backup (Simpan Data)**
```bash
# Method 1: Copy file (paling mudah)
copy db.sqlite3 backup_dd-mm-yyyy.sqlite3

# Method 2: Export to SQL
python manage.py dumpdata > backup.json
```

#### **Restore (Kembalikan Data)**
```bash
# Method 1: Ganti file
copy backup_dd-mm-yyyy.sqlite3 db.sqlite3

# Method 2: Import from JSON
python manage.py loaddata backup.json
```

### **🛠️ Database Management**

#### **Melihat Data via Admin**
1. Buka: `http://127.0.0.1:8000/admin/`
2. Login dengan superuser yang sudah dibuat
3. Kelola data Week dan Activity

#### **Reset Database (Hapus Semua Data)**
```bash
# Hati-hati! Ini akan menghapus semua data
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser  # optional
```

#### **Database Commands**
```bash
# Lihat struktur database
python manage.py dbshell

# Buat backup otomatis
python manage.py dumpdata tracker.week tracker.activity > my_data.json
```

---

## 🚀 **Aplikasi Personal - Tanpa Login**

### **🎯 Fitur yang Disederhanakan:**

#### ✅ **Yang TETAP ADA:**
- ✅ Dashboard mingguan dengan progress bar
- ✅ CRUD aktivitas (Tambah, Edit, Hapus)
- ✅ Toggle checkbox tanpa reload (AJAX)
- ✅ Navigasi minggu (sebelumnya/berikutnya)
- ✅ Jadwal default (Kuliah, Ibadah, dll)
- ✅ Statistik keseluruhan
- ✅ Admin panel untuk kelola data

#### ❌ **Yang DIHAPUS:**
- ❌ Sistem login/register
- ❌ Multiple users
- ❌ User profiles
- ❌ Authentication decorators

### **🏠 Homepage & Navigation**
- **Homepage**: Langsung redirect ke Dashboard
- **Navbar**: Dashboard, Statistik, Admin
- **No Login Required**: Langsung bisa digunakan!

### **📊 Halaman Statistik**
Akses di: `http://127.0.0.1:8000/stats/`
- Total minggu yang sudah ditrack
- Total aktivitas yang dibuat
- Jumlah aktivitas yang diselesaikan
- Persentase completion rate
- Achievement badges
- Info database SQLite

---

## 🔄 **Cara Menggunakan**

### **1. Akses Aplikasi**
```
URL: http://127.0.0.1:8000/
Langsung masuk ke Dashboard - tidak perlu login!
```

### **2. Dashboard Features**
- **Week Navigation**: Klik panah untuk lihat minggu lain
- **Progress Bar**: Otomatis update saat aktivitas di-check
- **Add Activity**: Klik tombol + pada card hari
- **Toggle Complete**: Klik checkbox untuk mark done
- **Edit/Delete**: Menu 3 dots pada aktivitas (kecuali default)

### **3. Default Schedule**
Aktivitas ini otomatis tersedia setiap minggu:
- **Selasa**: Kuliah (07:30-15:30) 
- **Kamis**: Kuliah (07:30-12:00)
- **Sabtu**: Latihan Ibadah Naposo
- **Minggu**: Ibadah Gereja Pagi

### **4. Custom Activities**
- Tambah aktivitas personal: belajar, olahraga, tugas, dll
- Set waktu (optional): "14:00-16:00" atau "2 jam"
- Edit/hapus kapan saja (kecuali yang default)

---

## 🎨 **Customization**

### **Mengubah Default Activities**
Edit file: `tracker/models.py` - method `create_default_activities()`:
```python
default_activities = [
    {'day': 'senin', 'name': 'Olahraga Pagi', 'time': '06:00-07:00', 'is_default': True},
    {'day': 'selasa', 'name': 'Kuliah', 'time': '07:30-15:30', 'is_default': True},
    # Tambah/edit sesuai kebutuhan
]
```

### **Mengubah Colors/Theme**
Edit file: `templates/base.html` - bagian `<style>`:
```css
/* Ganti primary color */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Ganti progress bar color */  
background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
```

---

## 📱 **Mobile & Responsive**

### **Mobile Friendly**
- Bootstrap 5 responsive grid
- Touch-friendly buttons dan checkboxes
- Optimized untuk semua screen sizes
- Smooth scrolling dan animations

### **PWA Ready** (Optional Future)
Bisa dikembangkan menjadi Progressive Web App:
- Install sebagai app di phone
- Offline capability
- Push notifications

---

## 🔧 **Development & Production**

### **Development Mode**
```bash
# Current settings
DEBUG = True
Database: SQLite (db.sqlite3)
Server: Django Development Server
```

### **Production Deployment** (Jika diperlukan)
```python
# settings.py changes
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']

# Use PostgreSQL for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # ... config
    }
}
```

---

## 🎯 **Performance & Tips**

### **Database Size**
- SQLite very lightweight
- 1 tahun data ≈ 1-5 MB
- Backup penting dilakukan rutin

### **Speed Optimization**
- AJAX untuk toggle tanpa reload
- Efficient database queries
- Minimal external dependencies

### **Best Practices**
- Backup data secara berkala
- Check aplikasi berjalan di background
- Monitor disk space (meski minimal)

---

## 🆘 **Troubleshooting**

### **Database Issues**
```bash
# Database corrupt?
del db.sqlite3
python manage.py migrate

# Data hilang?
copy backup.sqlite3 db.sqlite3
```

### **Server Issues**
```bash
# Port 8000 sudah digunakan?
python manage.py runserver 8001

# Permission issues?
Pastikan folder writable
```

### **Performance Slow**
```bash
# Reset database untuk clean start
python manage.py flush
```

---

## ✨ **Kesimpulan**

**Aplikasi Personal Pola Hidup Tracker** sudah siap digunakan dengan:

- 🚀 **No Login Required** - Langsung pakai!
- 🗄️ **SQLite Database** - Ringan dan simple
- 📊 **Full Features** - Dashboard, statistics, CRUD
- 📱 **Responsive Design** - Desktop & mobile friendly
- 🔧 **Easy Backup** - Copy file saja
- 🎨 **Professional UI** - Bootstrap 5 + custom styling

**Perfect untuk penggunaan personal!** 🎯

**Server berjalan di**: `http://127.0.0.1:8000/`
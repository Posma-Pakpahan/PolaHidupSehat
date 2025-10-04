from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
import calendar

class Week(models.Model):
    """Model untuk menyimpan data mingguan per user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weeks')
    start_date = models.DateField()  # Tanggal Senin
    end_date = models.DateField()    # Tanggal Minggu
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']
        unique_together = ['user', 'start_date']  # User bisa punya satu week per start_date

    def __str__(self):
        return f"{self.user.username} - Week {self.start_date} - {self.end_date}"

    @classmethod
    def get_or_create_current_week(cls, user):
        """Mendapatkan atau membuat week untuk minggu ini untuk user tertentu"""
        today = timezone.now().date()
        # Mendapatkan hari Senin dari minggu ini (0=Senin, 6=Minggu)
        days_since_monday = today.weekday()
        start_date = today - timedelta(days=days_since_monday)
        end_date = start_date + timedelta(days=6)
        
        week, created = cls.objects.get_or_create(
            user=user,
            start_date=start_date,
            defaults={'end_date': end_date}
        )
        return week

    @classmethod
    def get_week_by_offset(cls, user, offset=0):
        """Mendapatkan week berdasarkan offset dari minggu ini untuk user tertentu"""
        today = timezone.now().date()
        days_since_monday = today.weekday()
        base_start_date = today - timedelta(days=days_since_monday)
        start_date = base_start_date + timedelta(weeks=offset)
        end_date = start_date + timedelta(days=6)
        
        week, created = cls.objects.get_or_create(
            user=user,
            start_date=start_date,
            defaults={'end_date': end_date}
        )
        return week

    def get_days(self):
        """Mendapatkan semua hari dalam minggu ini"""
        days = []
        for i in range(7):
            date = self.start_date + timedelta(days=i)
            day_name = calendar.day_name[date.weekday()]
            days.append({
                'date': date,
                'name': day_name,
                'name_id': ['senin', 'selasa', 'rabu', 'kamis', 'jumat', 'sabtu', 'minggu'][i]
            })
        return days

    def get_progress_percentage(self):
        """Menghitung persentase progress untuk minggu ini"""
        total_activities = Activity.objects.filter(week=self).count()
        if total_activities == 0:
            return 0
        completed_activities = Activity.objects.filter(week=self, completed=True).count()
        return round((completed_activities / total_activities) * 100)


class Activity(models.Model):
    """Model untuk aktivitas harian"""
    DAYS_CHOICES = [
        ('senin', 'Senin'),
        ('selasa', 'Selasa'),
        ('rabu', 'Rabu'),
        ('kamis', 'Kamis'),
        ('jumat', 'Jumat'),
        ('sabtu', 'Sabtu'),
        ('minggu', 'Minggu'),
    ]

    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name='activities')
    day = models.CharField(max_length=10, choices=DAYS_CHOICES)
    name = models.CharField(max_length=200)
    time = models.CharField(max_length=50, blank=True, null=True)
    completed = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)  # Untuk aktivitas default seperti kuliah
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['day', 'created_at']

    def __str__(self):
        return f"{self.get_day_display()}: {self.name}"

    @classmethod
    def create_default_activities(cls, week):
        """Membuat aktivitas default pola hidup sehat berdasarkan jurnal kesehatan"""
        default_activities = [
            # SENIN - Hari Produktif & Fresh Start
            {'day': 'senin', 'name': 'Bangun Pagi & Doa Syukur', 'time': '05:30 - 05:35', 'is_default': True},
            {'day': 'senin', 'name': 'Baca Alkitab & Renungan', 'time': '05:35 - 05:45', 'is_default': True},
            {'day': 'senin', 'name': 'Olahraga Ringan/Stretching', 'time': '05:45 - 06:15', 'is_default': True},
            {'day': 'senin', 'name': 'Mandi & Persiapan', 'time': '06:15 - 06:45', 'is_default': True},
            {'day': 'senin', 'name': 'Sarapan Sehat', 'time': '06:45 - 07:15', 'is_default': True},
            {'day': 'senin', 'name': 'Waktu Belajar Fokus', 'time': '08:00 - 10:00', 'is_default': True},
            {'day': 'senin', 'name': 'Istirahat & Snack', 'time': '10:00 - 10:15', 'is_default': True},
            {'day': 'senin', 'name': 'Mengerjakan Tugas', 'time': '10:15 - 12:00', 'is_default': True},
            {'day': 'senin', 'name': 'Makan Siang', 'time': '12:00 - 13:00', 'is_default': True},
            {'day': 'senin', 'name': 'Istirahat Siang', 'time': '13:00 - 13:30', 'is_default': True},
            {'day': 'senin', 'name': 'Aktivitas Produktif', 'time': '13:30 - 17:00', 'is_default': True},
            {'day': 'senin', 'name': 'Olahraga Sore', 'time': '17:00 - 17:30', 'is_default': True},
            {'day': 'senin', 'name': 'Makan Malam', 'time': '18:30 - 19:30', 'is_default': True},
            {'day': 'senin', 'name': 'Family Time/Relaksasi', 'time': '19:30 - 21:00', 'is_default': True},
            {'day': 'senin', 'name': 'Doa Malam & Evaluasi Hari', 'time': '21:30 - 21:40', 'is_default': True},
            {'day': 'senin', 'name': 'Tidur', 'time': '22:00', 'is_default': True},

            # SELASA - Hari Kuliah Penuh
            {'day': 'selasa', 'name': 'Bangun Pagi & Doa Syukur', 'time': '05:00 - 05:05', 'is_default': True},
            {'day': 'selasa', 'name': 'Baca Alkitab & Renungan', 'time': '05:05 - 05:15', 'is_default': True},
            {'day': 'selasa', 'name': 'Persiapan Kuliah', 'time': '05:15 - 06:30', 'is_default': True},
            {'day': 'selasa', 'name': 'Sarapan Sehat', 'time': '06:30 - 07:00', 'is_default': True},
            {'day': 'selasa', 'name': 'Kuliah', 'time': '07:30 - 15:30', 'is_default': True},
            {'day': 'selasa', 'name': 'Istirahat & Snack', 'time': '15:30 - 16:00', 'is_default': True},
            {'day': 'selasa', 'name': 'Review Materi Kuliah', 'time': '16:00 - 17:00', 'is_default': True},
            {'day': 'selasa', 'name': 'Olahraga/Jalan Santai', 'time': '17:00 - 17:30', 'is_default': True},
            {'day': 'selasa', 'name': 'Makan Malam', 'time': '18:30 - 19:30', 'is_default': True},
            {'day': 'selasa', 'name': 'Waktu Belajar Mandiri', 'time': '19:30 - 21:30', 'is_default': True},
            {'day': 'selasa', 'name': 'Doa Malam & Refleksi', 'time': '21:30 - 21:40', 'is_default': True},
            {'day': 'selasa', 'name': 'Tidur', 'time': '22:00', 'is_default': True},

            # RABU - Hari Recovery & Pengembangan Diri
            {'day': 'rabu', 'name': 'Bangun Pagi & Doa Syukur', 'time': '05:30 - 05:35', 'is_default': True},
            {'day': 'rabu', 'name': 'Baca Alkitab & Renungan', 'time': '05:35 - 05:45', 'is_default': True},
            {'day': 'rabu', 'name': 'Olahraga Pagi', 'time': '05:45 - 06:30', 'is_default': True},
            {'day': 'rabu', 'name': 'Mandi & Persiapan', 'time': '06:30 - 07:00', 'is_default': True},
            {'day': 'rabu', 'name': 'Sarapan Sehat', 'time': '07:00 - 07:30', 'is_default': True},
            {'day': 'rabu', 'name': 'Waktu Belajar Fokus', 'time': '08:00 - 10:00', 'is_default': True},
            {'day': 'rabu', 'name': 'Istirahat & Snack', 'time': '10:00 - 10:15', 'is_default': True},
            {'day': 'rabu', 'name': 'Skill Development/Hobi', 'time': '10:15 - 12:00', 'is_default': True},
            {'day': 'rabu', 'name': 'Makan Siang', 'time': '12:00 - 13:00', 'is_default': True},
            {'day': 'rabu', 'name': 'Power Nap/Istirahat', 'time': '13:00 - 13:30', 'is_default': True},
            {'day': 'rabu', 'name': 'Proyek Personal', 'time': '13:30 - 16:00', 'is_default': True},
            {'day': 'rabu', 'name': 'Olahraga Sore', 'time': '16:00 - 16:30', 'is_default': True},
            {'day': 'rabu', 'name': 'Sosialisasi/Me Time', 'time': '16:30 - 18:00', 'is_default': True},
            {'day': 'rabu', 'name': 'Makan Malam', 'time': '18:30 - 19:30', 'is_default': True},
            {'day': 'rabu', 'name': 'Reading/Learning', 'time': '19:30 - 21:00', 'is_default': True},
            {'day': 'rabu', 'name': 'Doa Malam & Gratitude', 'time': '21:30 - 21:40', 'is_default': True},
            {'day': 'rabu', 'name': 'Tidur', 'time': '22:00', 'is_default': True},

            # KAMIS - Hari Kuliah
            {'day': 'kamis', 'name': 'Bangun Pagi & Doa Syukur', 'time': '05:00 - 05:05', 'is_default': True},
            {'day': 'kamis', 'name': 'Baca Alkitab & Renungan', 'time': '05:05 - 05:15', 'is_default': True},
            {'day': 'kamis', 'name': 'Persiapan Kuliah', 'time': '05:15 - 06:30', 'is_default': True},
            {'day': 'kamis', 'name': 'Sarapan Sehat', 'time': '06:30 - 07:00', 'is_default': True},
            {'day': 'kamis', 'name': 'Kuliah', 'time': '07:30 - 12:00', 'is_default': True},
            {'day': 'kamis', 'name': 'Makan Siang', 'time': '12:00 - 13:00', 'is_default': True},
            {'day': 'kamis', 'name': 'Istirahat', 'time': '13:00 - 13:30', 'is_default': True},
            {'day': 'kamis', 'name': 'Waktu Belajar Fokus', 'time': '13:30 - 15:30', 'is_default': True},
            {'day': 'kamis', 'name': 'Istirahat & Snack', 'time': '15:30 - 16:00', 'is_default': True},
            {'day': 'kamis', 'name': 'Aktivitas Fisik', 'time': '16:00 - 17:00', 'is_default': True},
            {'day': 'kamis', 'name': 'Relaksasi/Hobi', 'time': '17:00 - 18:30', 'is_default': True},
            {'day': 'kamis', 'name': 'Makan Malam', 'time': '18:30 - 19:30', 'is_default': True},
            {'day': 'kamis', 'name': 'Persiapan Weekend', 'time': '19:30 - 21:00', 'is_default': True},
            {'day': 'kamis', 'name': 'Doa Malam & Refleksi', 'time': '21:30 - 21:40', 'is_default': True},
            {'day': 'kamis', 'name': 'Tidur', 'time': '22:00', 'is_default': True},

            # JUMAT - Hari Persiapan Weekend
            {'day': 'jumat', 'name': 'Bangun Pagi & Doa Syukur', 'time': '05:30 - 05:35', 'is_default': True},
            {'day': 'jumat', 'name': 'Baca Alkitab & Renungan', 'time': '05:35 - 05:45', 'is_default': True},
            {'day': 'jumat', 'name': 'Olahraga Pagi', 'time': '05:45 - 06:30', 'is_default': True},
            {'day': 'jumat', 'name': 'Mandi & Persiapan', 'time': '06:30 - 07:00', 'is_default': True},
            {'day': 'jumat', 'name': 'Sarapan Sehat', 'time': '07:00 - 07:30', 'is_default': True},
            {'day': 'jumat', 'name': 'Waktu Belajar Intensif', 'time': '08:00 - 10:00', 'is_default': True},
            {'day': 'jumat', 'name': 'Istirahat & Snack', 'time': '10:00 - 10:15', 'is_default': True},
            {'day': 'jumat', 'name': 'Menyelesaikan Tugas', 'time': '10:15 - 12:00', 'is_default': True},
            {'day': 'jumat', 'name': 'Makan Siang', 'time': '12:00 - 13:00', 'is_default': True},
            {'day': 'jumat', 'name': 'Istirahat Siang', 'time': '13:00 - 13:30', 'is_default': True},
            {'day': 'jumat', 'name': 'Review & Planning', 'time': '13:30 - 15:00', 'is_default': True},
            {'day': 'jumat', 'name': 'Cleaning & Organizing', 'time': '15:00 - 16:00', 'is_default': True},
            {'day': 'jumat', 'name': 'Aktivitas Sosial', 'time': '16:00 - 18:00', 'is_default': True},
            {'day': 'jumat', 'name': 'Makan Malam', 'time': '18:30 - 19:30', 'is_default': True},
            {'day': 'jumat', 'name': 'Family/Friend Time', 'time': '19:30 - 21:30', 'is_default': True},
            {'day': 'jumat', 'name': 'Doa Malam & Syukur', 'time': '21:30 - 21:40', 'is_default': True},
            {'day': 'jumat', 'name': 'Tidur', 'time': '22:30', 'is_default': True},

            # SABTU - Hari Ibadah & Pelayanan
            {'day': 'sabtu', 'name': 'Bangun Pagi & Doa Syukur', 'time': '06:00 - 06:05', 'is_default': True},
            {'day': 'sabtu', 'name': 'Baca Alkitab & Renungan', 'time': '06:05 - 06:20', 'is_default': True},
            {'day': 'sabtu', 'name': 'Olahraga Pagi', 'time': '06:20 - 07:00', 'is_default': True},
            {'day': 'sabtu', 'name': 'Persiapan Ibadah', 'time': '07:00 - 08:00', 'is_default': True},
            {'day': 'sabtu', 'name': 'Sarapan Sehat', 'time': '08:00 - 08:30', 'is_default': True},
            {'day': 'sabtu', 'name': 'Latihan Ibadah Naposo', 'time': '09:00 - 12:00', 'is_default': True},
            {'day': 'sabtu', 'name': 'Makan Siang Bersama', 'time': '12:00 - 13:30', 'is_default': True},
            {'day': 'sabtu', 'name': 'Fellowship & Sharing', 'time': '13:30 - 15:00', 'is_default': True},
            {'day': 'sabtu', 'name': 'Personal Time/Istirahat', 'time': '15:00 - 16:30', 'is_default': True},
            {'day': 'sabtu', 'name': 'Aktivitas Rekreasi', 'time': '16:30 - 18:00', 'is_default': True},
            {'day': 'sabtu', 'name': 'Makan Malam', 'time': '18:30 - 19:30', 'is_default': True},
            {'day': 'sabtu', 'name': 'Prepare for Sunday', 'time': '19:30 - 20:30', 'is_default': True},
            {'day': 'sabtu', 'name': 'Relaksasi & Hiburan', 'time': '20:30 - 21:30', 'is_default': True},
            {'day': 'sabtu', 'name': 'Doa Malam & Gratitude', 'time': '21:30 - 21:40', 'is_default': True},
            {'day': 'sabtu', 'name': 'Tidur', 'time': '22:30', 'is_default': True},

            # MINGGU - Hari Ibadah & Rest
            {'day': 'minggu', 'name': 'Bangun Pagi & Doa Syukur', 'time': '06:00 - 06:05', 'is_default': True},
            {'day': 'minggu', 'name': 'Baca Alkitab & Meditasi', 'time': '06:05 - 06:25', 'is_default': True},
            {'day': 'minggu', 'name': 'Persiapan Ibadah', 'time': '06:25 - 07:30', 'is_default': True},
            {'day': 'minggu', 'name': 'Sarapan Ringan', 'time': '07:30 - 08:00', 'is_default': True},
            {'day': 'minggu', 'name': 'Ibadah Gereja Pagi', 'time': '08:30 - 11:30', 'is_default': True},
            {'day': 'minggu', 'name': 'Fellowship & Komunitas', 'time': '11:30 - 12:30', 'is_default': True},
            {'day': 'minggu', 'name': 'Makan Siang Keluarga', 'time': '12:30 - 14:00', 'is_default': True},
            {'day': 'minggu', 'name': 'Quality Time Keluarga', 'time': '14:00 - 16:00', 'is_default': True},
            {'day': 'minggu', 'name': 'Mengerjakan Tugas Mingguan', 'time': '16:00 - 18:00', 'is_default': True},
            {'day': 'minggu', 'name': 'Makan Malam', 'time': '18:30 - 19:30', 'is_default': True},
            {'day': 'minggu', 'name': 'Planning Minggu Depan', 'time': '19:30 - 20:30', 'is_default': True},
            {'day': 'minggu', 'name': 'Relaksasi & Prepare', 'time': '20:30 - 21:30', 'is_default': True},
            {'day': 'minggu', 'name': 'Doa Malam & Refleksi', 'time': '21:30 - 21:45', 'is_default': True},
            {'day': 'minggu', 'name': 'Tidur', 'time': '22:00', 'is_default': True},
        ]
        
        for activity_data in default_activities:
            cls.objects.get_or_create(
                week=week,
                day=activity_data['day'],
                name=activity_data['name'],
                defaults={
                    'time': activity_data['time'],
                    'is_default': activity_data['is_default'],
                    'completed': False
                }
            )


class UserProfile(models.Model):
    """Model untuk menyimpan profil user extended"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=50, default='Asia/Jakarta')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile: {self.user.username}"
    
    @property
    def total_weeks(self):
        """Total minggu yang sudah dilacak"""
        return self.user.weeks.count()
    
    @property
    def total_activities(self):
        """Total aktivitas yang sudah dibuat"""
        return Activity.objects.filter(week__user=self.user).count()
    
    @property
    def completion_rate(self):
        """Persentase completion rate keseluruhan"""
        total = Activity.objects.filter(week__user=self.user).count()
        if total == 0:
            return 0
        completed = Activity.objects.filter(week__user=self.user, completed=True).count()
        return round((completed / total) * 100, 1)
    
    @property
    def current_streak(self):
        """Streak hari berturut-turut melakukan aktivitas"""
        # Implementasi sederhana - bisa dikembangkan lebih lanjut
        today = timezone.now().date()
        streak = 0
        check_date = today
        
        while True:
            day_activities = Activity.objects.filter(
                week__user=self.user,
                week__start_date__lte=check_date,
                week__end_date__gte=check_date
            )
            
            if not day_activities.exists():
                break
                
            completed_today = day_activities.filter(completed=True).count()
            total_today = day_activities.count()
            
            if total_today == 0 or completed_today / total_today < 0.5:  # 50% completion threshold
                break
                
            streak += 1
            check_date -= timedelta(days=1)
            
            if streak > 30:  # Prevent infinite loop
                break
                
        return streak

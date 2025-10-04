from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tracker.models import Week, Activity

class Command(BaseCommand):
    help = 'Menerapkan template pola hidup sehat untuk user tertentu atau semua user'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=str,
            help='Username untuk menerapkan template (default: semua user)',
        )
        parser.add_argument(
            '--clear-existing',
            action='store_true',
            help='Hapus aktivitas non-default yang ada sebelum menerapkan template',
        )
        parser.add_argument(
            '--current-week-only',
            action='store_true',
            help='Hanya terapkan template untuk minggu ini saja',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🎯 Menerapkan Template Pola Hidup Sehat...')
        )

        # Determine users to process
        if options['user']:
            try:
                users = [User.objects.get(username=options['user'])]
                self.stdout.write(f"👤 Target user: {options['user']}")
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"❌ User '{options['user']}' tidak ditemukan!")
                )
                return
        else:
            users = User.objects.all()
            self.stdout.write(f"👥 Target: Semua user ({users.count()} user)")

        total_created = 0
        total_users_processed = 0

        for user in users:
            self.stdout.write(f"\n👤 Processing user: {user.username}")
            
            if options['current_week_only']:
                # Hanya untuk minggu ini
                week = Week.get_or_create_current_week(user)
                weeks = [week]
                self.stdout.write(f"📅 Menerapkan template untuk minggu ini: {week}")
            else:
                # Untuk semua minggu user ini
                weeks = Week.objects.filter(user=user)
                if not weeks.exists():
                    # Jika belum ada minggu, buat minggu ini
                    week = Week.get_or_create_current_week(user)
                    weeks = [week]
                self.stdout.write(f"📅 Menerapkan template untuk {weeks.count()} minggu")

            user_activities_created = 0

            for week in weeks:
                self.stdout.write(f"  📍 Processing Week: {week.start_date} - {week.end_date}")
                
                if options['clear_existing']:
                    # Hapus aktivitas non-default
                    deleted_count = Activity.objects.filter(
                        week=week, 
                        is_default=False
                    ).delete()[0]
                    if deleted_count > 0:
                        self.stdout.write(f"    🗑️  Dihapus {deleted_count} aktivitas custom")

                # Hapus aktivitas default lama untuk diganti dengan template baru
                old_defaults = Activity.objects.filter(week=week, is_default=True)
                old_count = old_defaults.count()
                if old_count > 0:
                    old_defaults.delete()
                    self.stdout.write(f"    🔄 Dihapus {old_count} aktivitas default lama")

                # Terapkan template baru
                Activity.create_default_activities(week)
                
                # Hitung aktivitas yang dibuat
                new_activities = Activity.objects.filter(week=week, is_default=True)
                created_count = new_activities.count()
                user_activities_created += created_count
                
                self.stdout.write(f"    ✅ Dibuat {created_count} aktivitas template")

            total_created += user_activities_created
            total_users_processed += 1
            self.stdout.write(f"  📊 Total untuk {user.username}: {user_activities_created} aktivitas")

        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Template berhasil diterapkan!'
                f'\n👥 Users processed: {total_users_processed}'
                f'\n📊 Total: {total_created} aktivitas template dibuat'
                f'\n📱 Buka http://127.0.0.1:8000/ untuk melihat hasilnya'
            )
        )

        # Tampilkan ringkasan template
        self.stdout.write(
            self.style.WARNING(
                f'\n📋 Template Pola Hidup Sehat yang diterapkan:'
                f'\n🌅 Bangun pagi (05:00-06:00) dengan doa & baca Alkitab'
                f'\n🏃 Olahraga rutin (pagi/sore)'
                f'\n📚 Waktu belajar terjadwal (2 jam per hari)'
                f'\n🎓 Kuliah (Selasa penuh, Kamis pagi)'
                f'\n⛪ Aktivitas rohani (Sabtu latihan, Minggu ibadah)'
                f'\n📝 Waktu tugas (Senin & Minggu)'
                f'\n😴 Tidur teratur (22:00-22:30)'
                f'\n🍽️ Pola makan sehat 3x sehari'
            )
        )
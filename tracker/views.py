from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
import json
from .models import Week, Activity, UserProfile
from .forms import ActivityForm
from .auth_forms import CustomUserCreationForm

def home(request):
    """Homepage - tampilkan landing page atau redirect ke dashboard jika sudah login"""
    if request.user.is_authenticated:
        return redirect('tracker:dashboard')
    return render(request, 'tracker/home.html')

@login_required
def dashboard(request):
    """Dashboard utama - menampilkan tracker mingguan untuk user yang login"""
    # Ambil parameter week offset dari URL (default 0 = minggu ini)
    week_offset = int(request.GET.get('week', 0))
    
    # Dapatkan week berdasarkan offset untuk user yang login
    week = Week.get_week_by_offset(request.user, week_offset)
    
    # Buat aktivitas default jika week baru dibuat
    if not week.activities.exists():
        Activity.create_default_activities(week)
    
    # Ambil semua aktivitas untuk minggu ini dikelompokkan per hari
    activities_by_day = {}
    for day_choice in Activity.DAYS_CHOICES:
        day_key = day_choice[0]
        activities_by_day[day_key] = week.activities.filter(day=day_key).order_by('created_at')
    
    # Informasi minggu
    days = week.get_days()
    progress = week.get_progress_percentage()
    
    # Navigation info
    week_info = {
        'current_offset': week_offset,
        'is_current_week': week_offset == 0,
        'week_label': get_week_label(week_offset),
        'date_range': f"{week.start_date.strftime('%d/%m/%Y')} - {week.end_date.strftime('%d/%m/%Y')}"
    }
    
    context = {
        'week': week,
        'activities_by_day': activities_by_day,
        'days': days,
        'progress': progress,
        'week_info': week_info,
    }
    
    return render(request, 'tracker/dashboard.html', context)

@csrf_exempt
@login_required
def toggle_activity(request):
    """Toggle status completed aktivitas via AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            activity_id = data.get('activity_id')
            
            # Pastikan user hanya bisa toggle aktivitas miliknya sendiri
            activity = get_object_or_404(Activity, id=activity_id, week__user=request.user)
            activity.completed = not activity.completed
            activity.save()
            
            # Hitung ulang progress
            progress = activity.week.get_progress_percentage()
            
            return JsonResponse({
                'success': True,
                'completed': activity.completed,
                'progress': progress
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def add_activity(request):
    """Tambah aktivitas baru"""
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            week_offset = int(request.POST.get('week_offset', 0))
            week = Week.get_week_by_offset(request.user, week_offset)
            
            activity = form.save(commit=False)
            activity.week = week
            activity.save()
            
            messages.success(request, 'Aktivitas berhasil ditambahkan!')
            return redirect(f'tracker:dashboard?week={week_offset}')
    else:
        form = ActivityForm()
        week_offset = int(request.GET.get('week', 0))
        day = request.GET.get('day', 'senin')
        form.fields['day'].initial = day
    
    return render(request, 'tracker/add_activity.html', {
        'form': form,
        'week_offset': week_offset
    })

@login_required
def edit_activity(request, activity_id):
    """Edit aktivitas"""
    activity = get_object_or_404(Activity, id=activity_id, week__user=request.user)
    
    # Tidak bisa edit aktivitas default
    if activity.is_default:
        messages.error(request, 'Aktivitas default tidak dapat diedit!')
        return redirect('tracker:dashboard')
    
    week_offset = request.GET.get('week', 0)
    
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aktivitas berhasil diperbarui!')
            return redirect(f'tracker:dashboard?week={week_offset}')
    else:
        form = ActivityForm(instance=activity)
    
    return render(request, 'tracker/edit_activity.html', {
        'form': form,
        'activity': activity,
        'week_offset': week_offset
    })

@login_required
def delete_activity(request, activity_id):
    """Hapus aktivitas"""
    activity = get_object_or_404(Activity, id=activity_id, week__user=request.user)
    
    # Tidak bisa hapus aktivitas default
    if activity.is_default:
        messages.error(request, 'Aktivitas default tidak dapat dihapus!')
        return redirect('tracker:dashboard')
    
    week_offset = request.GET.get('week', 0)
    
    if request.method == 'POST':
        activity.delete()
        messages.success(request, 'Aktivitas berhasil dihapus!')
        return redirect(f'tracker:dashboard?week={week_offset}')
    
    return render(request, 'tracker/delete_activity.html', {
        'activity': activity,
        'week_offset': week_offset
    })

@login_required
def stats(request):
    """Halaman statistik untuk user yang login"""
    # Stats untuk user yang login
    total_weeks = Week.objects.filter(user=request.user).count()
    total_activities = Activity.objects.filter(week__user=request.user).count()
    completed_activities = Activity.objects.filter(week__user=request.user, completed=True).count()
    completion_rate = round((completed_activities / total_activities * 100) if total_activities > 0 else 0)
    
    context = {
        'stats': {
            'total_weeks': total_weeks,
            'total_activities': total_activities,
            'completed_activities': completed_activities,
            'completion_rate': completion_rate,
        }
    }
    
    return render(request, 'tracker/stats.html', context)

def register_view(request):
    """View untuk registrasi user baru"""
    if request.user.is_authenticated:
        return redirect('tracker:dashboard')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registrasi berhasil! Selamat datang di Pola Hidup Tracker!')
            return redirect('tracker:dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile_view(request):
    """View untuk melihat profil user"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        # Buat profile jika belum ada
        profile = UserProfile.objects.create(user=request.user)
    
    # Statistik user
    total_weeks = profile.total_weeks
    total_activities = profile.total_activities
    completion_rate = profile.completion_rate
    current_streak = profile.current_streak
    
    # Achievement logic
    achievements = []
    if total_weeks >= 1:
        achievements.append({'title': 'First Week', 'desc': 'Menyelesaikan minggu pertama'})
    if completion_rate >= 80:
        achievements.append({'title': 'High Achiever', 'desc': 'Completion rate di atas 80%'})
    if current_streak >= 7:
        achievements.append({'title': 'Week Warrior', 'desc': 'Konsisten selama seminggu'})
    if total_activities >= 100:
        achievements.append({'title': 'Century Club', 'desc': 'Lebih dari 100 aktivitas'})
    
    context = {
        'profile': profile,
        'total_weeks': total_weeks,
        'total_activities': total_activities,
        'completion_rate': completion_rate,
        'current_streak': current_streak,
        'achievements': achievements,
    }
    
    return render(request, 'tracker/profile.html', context)

def get_week_label(offset):
    """Helper function untuk mendapatkan label minggu"""
    if offset == 0:
        return "Minggu Ini"
    elif offset == 1:
        return "Minggu Depan"
    elif offset == -1:
        return "Minggu Lalu"
    elif offset > 1:
        return f"{offset} Minggu Ke Depan"
    else:
        return f"{abs(offset)} Minggu Lalu"

from django.contrib import admin
from .models import Week, Activity

@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'end_date', 'get_progress_percentage', 'created_at']
    list_filter = ['start_date', 'created_at']
    search_fields = ['start_date']
    readonly_fields = ['created_at', 'updated_at']

    def get_progress_percentage(self, obj):
        return f"{obj.get_progress_percentage()}%"
    get_progress_percentage.short_description = 'Progress'

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['name', 'day', 'week', 'completed', 'is_default', 'created_at']
    list_filter = ['day', 'completed', 'is_default', 'week__start_date']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']

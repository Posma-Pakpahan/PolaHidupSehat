from django import forms
from .models import Activity

class ActivityForm(forms.ModelForm):
    """Form untuk CRUD aktivitas"""
    
    class Meta:
        model = Activity
        fields = ['day', 'name', 'time']
        widgets = {
            'day': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: Belajar, Olahraga, Tugas',
                'required': True,
                'maxlength': 200
            }),
            'time': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: 08:00 - 10:00 (Opsional)',
                'maxlength': 50
            }),
        }
        labels = {
            'day': 'Hari',
            'name': 'Nama Aktivitas',
            'time': 'Waktu',
        }
        help_texts = {
            'time': 'Format waktu bersifat opsional. Contoh: 08:00 - 10:00 atau 2 jam',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Menambahkan CSS classes untuk styling Bootstrap
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        
        # Khusus untuk select day
        self.fields['day'].widget.attrs.update({'class': 'form-select'})
from django import forms
from .models import Produk

class ProdukForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = ['nama', 'kategori', 'harga', 'stok', 'status_halal', 'keterangan']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'kategori': forms.Select(attrs={'class': 'form-select'}),
            'harga': forms.NumberInput(attrs={'class': 'form-control'}),
            'stok': forms.NumberInput(attrs={'class': 'form-control'}),
            'status_halal': forms.Select(attrs={'class': 'form-select'}),
            'keterangan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
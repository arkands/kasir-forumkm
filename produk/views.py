from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Produk
from .forms import ProdukForm

@login_required
def daftar_produk(request):
    produk = Produk.objects.all()
    return render(request, 'produk/daftar_produk.html', {'produk': produk})

@login_required
def tambah_produk(request):
    if request.method == 'POST':
        form = ProdukForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('daftar_produk')
    else:
        form = ProdukForm()
    return render(request, 'produk/form_produk.html', {'form': form, 'judul': 'Tambah Produk'})

@login_required
def edit_produk(request, pk):
    produk = get_object_or_404(Produk, pk=pk)
    if request.method == 'POST':
        form = ProdukForm(request.POST, instance=produk)
        if form.is_valid():
            form.save()
            return redirect('daftar_produk')
    else:
        form = ProdukForm(instance=produk)
    return render(request, 'produk/form_produk.html', {'form': form, 'judul': 'Edit Produk'})

@login_required
def hapus_produk(request, pk):
    produk = get_object_or_404(Produk, pk=pk)
    if request.method == 'POST':
        produk.delete()
        return redirect('daftar_produk')
    return render(request, 'produk/konfirmasi_hapus.html', {'produk': produk})
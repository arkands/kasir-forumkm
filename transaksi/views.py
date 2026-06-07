from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaksi, ItemTransaksi
from produk.models import Produk

@login_required
def daftar_transaksi(request):
    transaksi = Transaksi.objects.all().order_by('-tanggal')
    return render(request, 'transaksi/daftar_transaksi.html', {'transaksi': transaksi})

@login_required
def kasir(request):
    produk_list = Produk.objects.filter(stok__gt=0)

    if request.method == 'POST':
        produk_ids = request.POST.getlist('produk_id')
        jumlah_list = request.POST.getlist('jumlah')
        metode_bayar = request.POST.get('metode_bayar', 'cash')
        uang_bayar = request.POST.get('uang_bayar', 0)

        transaksi = Transaksi.objects.create(total=0)
        total = 0

        for pid, jml in zip(produk_ids, jumlah_list):
            jml = int(jml)
            if jml <= 0:
                continue
            produk = Produk.objects.get(pk=pid)
            subtotal = produk.harga * jml
            total += subtotal
            ItemTransaksi.objects.create(
                transaksi=transaksi,
                produk=produk,
                jumlah=jml,
                harga_saat_beli=produk.harga,
                subtotal=subtotal
            )
            produk.stok -= jml
            produk.save()

        if total == 0:
            transaksi.delete()
            return redirect('kasir')

        transaksi.total = total
        transaksi.metode_bayar = metode_bayar

        if metode_bayar == 'cash':
            try:
                uang_bayar = int(uang_bayar)
            except (ValueError, TypeError):
                uang_bayar = total
            transaksi.uang_bayar = uang_bayar
            transaksi.kembalian = max(0, uang_bayar - total)
        else:
            transaksi.uang_bayar = total
            transaksi.kembalian = 0

        transaksi.save()
        return redirect('struk', pk=transaksi.pk)

    return render(request, 'transaksi/kasir.html', {'produk_list': produk_list})

@login_required
def struk(request, pk):
    transaksi = get_object_or_404(Transaksi, pk=pk)
    return render(request, 'transaksi/struk.html', {'transaksi': transaksi})
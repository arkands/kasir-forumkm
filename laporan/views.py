from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from transaksi.models import Transaksi
import json

@login_required
def laporan_harian(request):
    tanggal_str = request.GET.get('tanggal', '')
    if tanggal_str:
        from datetime import datetime
        tanggal = datetime.strptime(tanggal_str, '%Y-%m-%d').date()
    else:
        tanggal = timezone.now().date()

    transaksi = Transaksi.objects.filter(
        tanggal__date=tanggal
    ).order_by('-tanggal')

    total_omzet = transaksi.aggregate(Sum('total'))['total__sum'] or 0
    total_transaksi = transaksi.count()

    return render(request, 'laporan/laporan_harian.html', {
        'transaksi': transaksi,
        'tanggal': tanggal,
        'total_omzet': total_omzet,
        'total_transaksi': total_transaksi,
    })

@login_required
def laporan_bulanan(request):
    bulan = int(request.GET.get('bulan', timezone.now().month))
    tahun = int(request.GET.get('tahun', timezone.now().year))

    transaksi = Transaksi.objects.filter(
        tanggal__month=bulan,
        tanggal__year=tahun
    ).order_by('-tanggal')

    total_omzet = transaksi.aggregate(Sum('total'))['total__sum'] or 0
    total_transaksi = transaksi.count()

    from django.db.models.functions import TruncDate
    data_grafik = Transaksi.objects.filter(
        tanggal__month=bulan,
        tanggal__year=tahun
    ).annotate(
        tgl=TruncDate('tanggal')
    ).values('tgl').annotate(
        omzet=Sum('total')
    ).order_by('tgl')

    labels = [str(d['tgl']) for d in data_grafik]
    data = [float(d['omzet']) for d in data_grafik]

    return render(request, 'laporan/laporan_bulanan.html', {
        'transaksi': transaksi,
        'bulan': bulan,
        'tahun': tahun,
        'total_omzet': total_omzet,
        'total_transaksi': total_transaksi,
        'labels': json.dumps(labels),
        'data': json.dumps(data),
    })

@login_required
def info_harga(request):
    import requests as req
    data_harga = []
    error = None

    try:
        url = 'https://api.hargapangan.id/tabel/komoditas/pasar/provinsi/1/34'
        response = req.get(url, timeout=5)

        if response.status_code == 200:
            raw = response.json()
            for item in raw[:10]:
                data_harga.append({
                    'nama': item.get('komoditas', '-'),
                    'harga': item.get('harga', '-'),
                    'satuan': item.get('satuan', '-'),
                })
        else:
            error = 'Gagal mengambil data dari API'

    except Exception as e:
        error = f'Koneksi gagal: {str(e)}'
        data_harga = [
            {'nama': 'Beras Medium', 'harga': 'Rp 13.000', 'satuan': 'kg'},
            {'nama': 'Gula Pasir', 'harga': 'Rp 17.000', 'satuan': 'kg'},
            {'nama': 'Minyak Goreng', 'harga': 'Rp 19.000', 'satuan': 'liter'},
            {'nama': 'Tepung Terigu', 'harga': 'Rp 12.000', 'satuan': 'kg'},
            {'nama': 'Telur Ayam', 'harga': 'Rp 28.000', 'satuan': 'kg'},
        ]

    return render(request, 'laporan/info_harga.html', {
        'data_harga': data_harga,
        'error': error,
    })
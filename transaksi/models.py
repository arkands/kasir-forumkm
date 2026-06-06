from django.db import models
from produk.models import Produk

class Transaksi(models.Model):
    tanggal = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    catatan = models.TextField(blank=True)

    def __str__(self):
        return f"Transaksi #{self.pk} - {self.tanggal.strftime('%d/%m/%Y')}"

class ItemTransaksi(models.Model):
    transaksi = models.ForeignKey(Transaksi, on_delete=models.CASCADE, related_name='items')
    produk = models.ForeignKey(Produk, on_delete=models.PROTECT)
    jumlah = models.IntegerField(default=1)
    harga_saat_beli = models.DecimalField(max_digits=10, decimal_places=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=0)

    def __str__(self):
        return f"{self.produk.nama} x{self.jumlah}"
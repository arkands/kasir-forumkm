from django.db import models

class Kategori(models.Model):
    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama

class Produk(models.Model):
    STATUS_HALAL = [
        ('halal', 'Halal'),
        ('tidak_halal', 'Tidak Halal'),
        ('perlu_cek', 'Perlu Dicek'),
    ]

    nama = models.CharField(max_length=200)
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True)
    harga = models.DecimalField(max_digits=10, decimal_places=0)
    stok = models.IntegerField(default=0)
    status_halal = models.CharField(max_length=20, choices=STATUS_HALAL, default='perlu_cek')
    keterangan = models.TextField(blank=True)
    dibuat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama
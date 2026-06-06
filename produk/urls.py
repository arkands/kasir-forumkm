from django.urls import path
from . import views

urlpatterns = [
    path('', views.daftar_produk, name='daftar_produk'),
    path('tambah/', views.tambah_produk, name='tambah_produk'),
    path('edit/<int:pk>/', views.edit_produk, name='edit_produk'),
    path('hapus/<int:pk>/', views.hapus_produk, name='hapus_produk'),
]
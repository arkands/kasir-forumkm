from django.urls import path
from . import views

urlpatterns = [
    path('', views.laporan_harian, name='laporan_harian'),
    path('bulanan/', views.laporan_bulanan, name='laporan_bulanan'),
    path('harga/', views.info_harga, name='info_harga'),
]

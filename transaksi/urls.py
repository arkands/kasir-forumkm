from django.urls import path
from . import views

urlpatterns = [
    path('', views.daftar_transaksi, name='daftar_transaksi'),
    path('baru/', views.kasir, name='kasir'),
    path('struk/<int:pk>/', views.struk, name='struk'),
]
from django.urls import path
from .import views

urlpatterns = [
    path('data_entry/', views.set_data_entry, name='set_data_entry'),
    path('pengguna/', views.set_pengguna, name='set_pengguna'),
    path('pengguna/view/<id>', views.view_pengguna, name='view_pengguna'),
    path('api/pengguna/<int:user_id>/', views.get_pengguna_detail_api, name='get_pengguna_detail_api'),
    path('pengguna/<int:id>/edit/', views.update_pengguna, name='update_pengguna'),
    path('pengguna/<int:id>/delete/', views.delete_pengguna, name='delete_pengguna'),

     # Konten
    path('content/', views.set_content, name='set_content'),
    path('content/<int:id>/', views.view_content, name='view_content'),
    path('content/<int:id>/update/', views.update_content, name='update_content'),
    path('content/<int:id>/delete/', views.delete_content, name='delete_content'),


]
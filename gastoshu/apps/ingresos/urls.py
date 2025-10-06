from django.urls import path
from . import views

urlpatterns = [
    path('listado/', views.ingreso_list, name='ingreso_list'),
    path('crear/', views.ingreso_create, name='ingreso_create'),
    path('actualizar/<int:ingreso_id>/', views.ingreso_update, name='ingreso_update'),
    path('eliminar/<int:ingreso_id>/', views.ingreso_delete, name='ingreso_delete'),
]
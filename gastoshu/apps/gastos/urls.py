from django.urls import path
from . import views

urlpatterns = [
    path('listado/', views.gasto_list, name='gasto_list'),
    path('crear/', views.gasto_create, name='gasto_create'),
    path('actualizar/<int:gasto_id>/', views.gasto_update, name='gasto_update'),
    path('eliminar/<int:gasto_id>/', views.gasto_delete, name='gasto_delete'),
]

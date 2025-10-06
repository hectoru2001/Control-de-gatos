from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.login.urls')),
    path('inicio/', include('apps.dashboard.urls')),
    path('gastos/', include('apps.gastos.urls')),
    path('ingresos/', include('apps.ingresos.urls')),
]

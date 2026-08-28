from django.contrib import admin
from django.urls import path
from dispositivos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.listar_zonas, name='inicio'), # Esta línea soluciona el error en la raíz
    path('zonas/', views.listar_zonas, name='listar_zonas'),
    path('zonas/<int:zona_id>/', views.detalle_zona, name='detalle_zona'),
    path('resumen-zonas/', views.resumen_zonas, name='resumen_zonas'),
]
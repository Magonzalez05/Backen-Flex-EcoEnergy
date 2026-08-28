import json
import os
from django.conf import settings
from django.shortcuts import render
from django.http import Http404

def cargar_datos(nombre_archivo):
    ruta = os.path.join(settings.BASE_DIR, 'data', f'{nombre_archivo}.json')
    if not os.path.exists(ruta):
        return []
    with open(ruta, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

def listar_zonas(request):
    zonas = cargar_datos('zonas')
    dispositivos = cargar_datos('dispositivos')

    for zona in zonas:
        zona['cantidad_dispositivos'] = sum(1 for d in dispositivos if d.get('zona_id') == zona.get('id'))

    return render(request, 'zonas/listado.html', {'zonas': zonas})

def detalle_zona(request, zona_id):
    zonas = cargar_datos('zonas')
    dispositivos = cargar_datos('dispositivos')
    categorias = cargar_datos('categorias')

    # Buscar la zona por ID; si no existe, 404
    zona = next((z for z in zonas if z.get('id') == zona_id), None)
    if not zona:
        raise Http404("La zona solicitada no existe.")

    # Mapa de categorías para cruce rápido
    mapa_cat = {c['id']: c['nombre'] for c in categorias}

    # Filtrar dispositivos asociados y enriquecer con nombre de categoría
    dispositivos_zona = []
    consumo_total = 0.0
    for d in dispositivos:
        if d.get('zona_id') == zona_id:
            disp_info = d.copy()
            disp_info['categoria_nombre'] = mapa_cat.get(d.get('categoria_id'), 'Sin categoría')
            consumo_total += float(d.get('consumo_kwh', 0))
            dispositivos_zona.append(disp_info)

    limite = float(zona.get('limite_kwh', 0))
    estado = "ALERTA" if consumo_total > limite else "NORMAL"

    contexto = {
        'zona': zona,
        'dispositivos': dispositivos_zona,
        'consumo_total': round(consumo_total, 2),
        'cantidad_dispositivos': len(dispositivos_zona),
        'estado': estado,
    }
    return render(request, 'zonas/detalle.html', contexto)

def resumen_zonas(request):
    zonas = cargar_datos('zonas')
    dispositivos = cargar_datos('dispositivos')

    resumen = []
    total_consumo_general = 0.0

    for zona in zonas:
        z_id = zona.get('id')
        disps = [d for d in dispositivos if d.get('zona_id') == z_id]
        consumo_zona = sum(float(d.get('consumo_kwh', 0)) for d in disps)
        limite = float(zona.get('limite_kwh', 0))
        
        estado = "LÍMITE SUPERADO" if consumo_zona > limite else "DENTRO DEL LÍMITE"
        
        total_consumo_general += consumo_zona
        resumen.append({
            'id': z_id,
            'nombre': zona.get('nombre'),
            'cantidad_dispositivos': len(disps),
            'consumo_total': round(consumo_zona, 2),
            'limite_kwh': limite,
            'estado': estado
        })

    contexto = {
        'resumen': resumen,
        'total_zonas': len(zonas),
        'total_dispositivos': len(dispositivos),
        'total_consumo_general': round(total_consumo_general, 2)
    }
    return render(request, 'zonas/resumen.html', contexto)











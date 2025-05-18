from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Campo, Lote, ArchivoDato, DatoGeo, ArchivoLote
from .forms import UploadArchivoForm
from django.contrib.auth.models import User
import shapefile,os, csv
import numpy as np
import tempfile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os, json
import geopandas as gpd
from .models import ArchivoLote, Lote


@login_required
def upload_archivos(request):
    
    return render(request, 'upload.html')

@login_required
def carga_archivos(request):
    empresa = request.user.profile.empresa

    if request.method == 'POST':
        form = UploadArchivoForm(empresa, request.POST, request.FILES)

        if form.is_valid():
            lote = form.cleaned_data['lote']
            nombre = form.cleaned_data['nombre']
            archivos = request.FILES.getlist('archivos')
            tipo = nombre.lower().strip().replace(" ", "_")  # se convierte en el "tipo" de la capa


            if not archivos:
                messages.error(request, "Debe subir al menos un archivo.")
                return redirect('carga_archivos')

            # Agrupar archivos por nombre base
            conjuntos = {}
            for archivo in archivos:
                base = archivo.name.split('.')[0]
                conjuntos.setdefault(base, []).append(archivo)

            for base, grupo in conjuntos.items():
                tmpdir = tempfile.mkdtemp()

                for archivo in grupo:
                    archivo_nombre = archivo.name
                    extension = archivo_nombre.split('.')[-1].lower()
                    ruta_destino = os.path.join(tmpdir, archivo_nombre)

                    with open(ruta_destino, 'wb+') as destino:
                        for chunk in archivo.chunks():
                            destino.write(chunk)

                    # Guardar el archivo original
                    ArchivoLote.objects.create(
                        lote=lote,
                        nombre=archivo_nombre,
                        archivo=archivo,
                        extension=extension,
                        tipo=tipo
                    )

                # Convertir el .shp a GeoJSON y guardar
                try:
                    shp_file = next((f.name for f in grupo if f.name.endswith('.shp')), None)
                    if shp_file:
                        full_path = os.path.join(tmpdir, shp_file)
                        gdf = gpd.read_file(full_path)
                        geojson_str = gdf.to_json()

                        geojson_filename = f"{base}.geojson"
                        geojson_path = default_storage.save(
                            f"lotes/{geojson_filename}",
                            ContentFile(geojson_str.encode('utf-8'))
                        )

                        ArchivoLote.objects.create(
                            lote=lote,
                            nombre=geojson_filename,
                            archivo=geojson_path,
                            extension='geojson',
                            tipo=tipo
                        )
                except Exception as e:
                    print(f" Error al convertir {base} a GeoJSON: {e}")
                    messages.warning(request, f"Error al generar GeoJSON para {base}: {e}")

            messages.success(request, f"Archivos de '{nombre}' cargados correctamente.")
            return redirect('carga_archivos')
        else:
            messages.error(request, "Errores en el formulario.")
    else:
        form = UploadArchivoForm(empresa)

    return render(request, 'carga_archivos.html', {'form': form})

@login_required
def mapa_shapefile(request):
    empresa = request.user.profile.empresa
    form = UploadArchivoForm(empresa)
    return render(request, "mapa_shapefile.html", {"form": form})

@login_required
def get_capas_lote(request):
    lote_id = request.GET.get('lote_id')
    print(f"📥 Lote ID recibido: {lote_id}")

    try:
        archivos = ArchivoLote.objects.filter(lote_id=lote_id, extension='geojson')
    except Exception as e:
        print(f" Error al filtrar archivos: {e}")
        return JsonResponse({"error": "Error interno del servidor."}, status=500)

    print(f"📦 Archivos .geojson encontrados: {archivos.count()}")

    tipos_detectados = set()
    resultado = []
    for archivo in archivos:
        tipos_detectados.add(archivo.tipo)
        print(f" Archivo: {archivo.nombre} | Tipo: {archivo.tipo} | Fecha: {archivo.fecha_carga.strftime('%Y-%m-%d %H:%M')}")
        resultado.append({
            "nombre": archivo.nombre,
            "url": archivo.archivo.url,
            "extension": archivo.extension,
            "tipo": archivo.tipo,
            "tipo": archivo.tipo,
            "fecha": archivo.fecha_carga.strftime('%Y-%m-%d %H:%M'),
        })

    print(f" Tipos únicos de capas: {sorted(list(tipos_detectados))} → Total: {len(tipos_detectados)}")

    return JsonResponse({"capas": resultado})



@login_required
def get_capa_tipo(request):
    lote_id = request.GET.get('lote_id')
    tipo = request.GET.get('tipo')

    print(f" Petición de capa tipo: lote_id={lote_id}, tipo={tipo}")

    archivos = ArchivoLote.objects.filter(lote_id=lote_id, tipo=tipo, extension='geojson').order_by('-fecha_carga')

    print(f" Archivos encontrados: {archivos.count()}")
    resultado = []
    geojson_dict = {}

    # Paletas de colores por tipo
    paleta_semaforo = [
        "#00ff00",  # Verde fuerte
        "#66ff00",  # Verde claro
        "#ccff00",  # Amarillo verdoso
        "#ffff00",  # Amarillo puro
        "#ffcc00",  # Amarillo anaranjado
        "#ff9900",  # Naranja
        "#ff6600",  # Naranja fuerte
        "#ff3300",  # Rojo anaranjado
        "#ff0000",  # Rojo puro
        "#990000",  # Rojo oscuro
    ]

    paletas = {
        'nitrogeno': [...],
        'fosforo': [...],
        'fertilizante': [...]
    }

    leyenda = []
    estadisticas = {}

    if archivos.exists():
        archivo = archivos.first()
        print(f" Procesando archivo: {archivo.nombre}")
        try:
            gdf = gpd.read_file(archivo.archivo.path)

            if 'rate' in gdf.columns:
                min_rate = gdf['rate'].min()
                max_rate = gdf['rate'].max()
                print(f" Rango 'rate': {min_rate} a {max_rate}")

                valores_validos = gdf['rate'].dropna()
                if not valores_validos.empty and tipo == 'cosecha':
                    estadisticas = {
                        'min': round(valores_validos.min(), 2),
                        'max': round(valores_validos.max(), 2),
                        'prom': round(valores_validos.mean(), 2)
                    }

                bins = np.linspace(min_rate, max_rate, 11)
                etiquetas = [f"{int(bins[i])} - {int(bins[i+1])}" for i in range(10)]

                colores = paleta_semaforo if tipo == 'cosecha' else paletas.get(tipo, ['#999999'] * 10)

                leyenda = [{"rango": r, "color": c} for r, c in zip(etiquetas, colores)]
                print(f" Leyenda armada: {len(leyenda)} clases")

            else:
                print("⚠️ No hay columna 'rate'.")
                gdf['color'] = "#000000"

            geojson_dict = json.loads(gdf.to_json())

        except Exception as e:
            print(" Error al leer archivo para leyenda:", str(e))
            leyenda = []

    for archivo in archivos:
        resultado.append({
            'nombre': archivo.nombre,
            'url': archivo.archivo.url,
            'extension': archivo.extension,
            'fecha': archivo.fecha_carga.strftime('%Y-%m-%d %H:%M'),
        })

    if gdf.empty:
        print("⚠️ GeoDataFrame vacío, no se genera GeoJSON.")
        geojson_dict = {"type": "FeatureCollection", "features": []}
    else:
        geojson_dict = json.loads(gdf.to_json())

    return JsonResponse({
        'capas': resultado,
        'leyenda': leyenda,
        'estadisticas': estadisticas,
        'geojson': geojson_dict  # Esto faltaba
    })

@login_required
def ajax_lotes_por_campo(request):
    campo_id = request.GET.get('campo_id')
    lotes = Lote.objects.filter(campo_id=campo_id).order_by('nombre')
    data = [{"id": lote.id, "nombre": lote.nombre} for lote in lotes]
    return JsonResponse({"lotes": data})


@login_required
def analizar_mapas(request):
    empresa = request.user.profile.empresa
    form = UploadArchivoForm(empresa)
    return render(request, 'analizar_mapas.html',{'form': form})

def analizar_mapas_cocecha(request):
    empresa = request.user.profile.empresa
    form = UploadArchivoForm(empresa)
    return render(request, 'analizar_mapa_cocecha.html',{'form': form})


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import ArchivoLote
import json
import numpy as np
import os
from django.views.decorators.http import require_GET

@login_required
def api_mapa_lote(request):
    lote_id = request.GET.get('lote_id')
    print(f" Lote recibido para análisis: {lote_id}")

    archivos = ArchivoLote.objects.filter(
        lote_id=lote_id, tipo='cosecha', extension='geojson'
    ).order_by('-fecha_carga')

    print(f"🔎 Archivos encontrados: {archivos.count()}")

    if not archivos.exists():
        print(" No se encontró archivo de cosecha")
        return JsonResponse({"error": "No se encontró archivo de cosecha"}, status=404)

    archivo = archivos.first()
    print(f" Archivo usado: {archivo.nombre}")

    try:
        with open(archivo.archivo.path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        features = data.get('features', [])
        print(f" Cantidad de features: {len(features)}")

        if not features:
            return JsonResponse({"error": "GeoJSON sin features"}, status=400)

        # Recolectar valores de 'rate'
        rates = []
        for feat in features:
            props = feat.get('properties', {})
            if 'rate' in props:
                rates.append(props['rate'])

        if not rates:
            return JsonResponse({"error": "No hay datos de 'rate'"}, status=400)

        rates = np.array(rates)
        min_rate, max_rate = rates.min(), rates.max()
        bins = np.linspace(min_rate, max_rate, 11)
        print(f" Bins de rendimiento: {bins}")

        etiquetas = [f"{int(bins[i])}-{int(bins[i+1])}" for i in range(10)]

        # Paleta invertida: verde = mejor rendimiento
        colores = [
           "#ff0000", "#ff3300", "#ff6600", "#ff9900", "#ffcc00",
           "#ccff00", "#99ff00", "#66ff00", "#33ff00", "#00ff00"
        ]

        # Asignar color y contar hectáreas por rango
        conteo_rangos = {etiquetas[i]: 0 for i in range(10)}

        for feat in features:
            props = feat.get('properties', {})
            rate = props.get('rate')

            if rate is None:
                continue

            idx = np.digitize(rate, bins) - 1
            idx = max(0, min(idx, 9))

            etiqueta = etiquetas[idx]
            conteo_rangos[etiqueta] += 0.003  # 30 m² ≈ 0.003 ha
            props['color'] = colores[idx]

        #  Estadísticas
        estadisticas = {
            'minimo': round(float(rates.min()), 2),
            'maximo': round(float(rates.max()), 2),
            'promedio': round(float(rates.mean()), 2),
            'mediana': round(float(np.median(rates)), 2),
            'desvio_std': round(float(np.std(rates)), 2),
            'coef_variacion': round(float(np.std(rates) / rates.mean()) * 100, 2)
        }

        print(f"Estadísticas: {estadisticas}")
        print(f" Rango ha por clase: {conteo_rangos}")
        print(" Enviado al cliente:")
        print(" - Estadísticas:", estadisticas)
        print(" - Rangos por ha:", {k: round(v, 2) for k, v in conteo_rangos.items()})

        return JsonResponse({
            "geojson": data,
            "estadisticas": estadisticas,
            "rangos_hectareas": conteo_rangos
        })

    except Exception as e:
        print(" Error al procesar GeoJSON:", str(e))
        return JsonResponse({"error": "Error procesando el archivo"}, status=500)
from django.views.decorators.http import require_GET
from django.http import JsonResponse
import json
from .models import ArchivoLote

@require_GET
def get_capas_selecc(request):
    print("✅ ENTRÓ A get_capas_selecc")

    tipo = request.GET.get('tipo')
    lote_id = request.GET.get('lote_id')
    print(f"📥 tipo={tipo}, lote_id={lote_id}")

    if not tipo or not lote_id:
        print("⚠️ Faltan parámetros")
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)

    try:
        archivo = ArchivoLote.objects.filter(tipo=tipo, lote_id=lote_id, extension='geojson').first()
        print(f"📦 archivo encontrado: {archivo}")

        if not archivo or not archivo.archivo:
            print("❌ Archivo no encontrado o vacío")
            return JsonResponse({'error': 'No se encontró capa'}, status=404)

        with open(archivo.archivo.path, 'r', encoding='utf-8') as f:
            geojson = json.load(f)

        print("✅ GeoJSON cargado correctamente")
        return JsonResponse({'geojson': geojson})

    except Exception as e:
        print(f"💥 Error inesperado: {e}")
        return JsonResponse({'error': str(e)}, status=500)






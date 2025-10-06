from django.shortcuts import render
from django.db.models import Sum
from apps.gastos.models import Gasto
from apps.ingresos.models import Ingresos
from django.utils import timezone
from datetime import timedelta

def inicio(request):
    # Totales generales
    total_gastos = Gasto.objects.aggregate(total=Sum("monto"))["total"] or 0
    total_ingresos = Ingresos.objects.aggregate(total=Sum("monto"))["total"] or 0
    balance = total_ingresos - total_gastos
    
    # Conteo de transacciones
    gastos_count = Gasto.objects.count()
    ingresos_count = Ingresos.objects.count()
    
    # Tasa de ahorro
    tasa_ahorro = (balance / total_ingresos * 100) if total_ingresos > 0 else 0
    
    # Fechas para filtros
    hoy = timezone.now().date()
    inicio_mes_actual = hoy.replace(day=1)
    inicio_mes_anterior = (inicio_mes_actual - timedelta(days=1)).replace(day=1)
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    inicio_anio = hoy.replace(month=1, day=1)
    
    # Gastos por período
    gastos_hoy = Gasto.objects.filter(fecha=hoy).aggregate(total=Sum("monto"))["total"] or 0
    gastos_semana = Gasto.objects.filter(fecha__gte=inicio_semana).aggregate(total=Sum("monto"))["total"] or 0
    gastos_mes_actual = Gasto.objects.filter(fecha__gte=inicio_mes_actual).aggregate(total=Sum("monto"))["total"] or 0
    gastos_mes_anterior = Gasto.objects.filter(
        fecha__gte=inicio_mes_anterior, 
        fecha__lt=inicio_mes_actual
    ).aggregate(total=Sum("monto"))["total"] or 0
    gastos_anio_actual = Gasto.objects.filter(fecha__gte=inicio_anio).aggregate(total=Sum("monto"))["total"] or 0
    
    # Ingresos por período
    ingresos_mes_actual = Ingresos.objects.filter(fecha__gte=inicio_mes_actual).aggregate(total=Sum("monto"))["total"] or 0
    ingresos_mes_anterior = Ingresos.objects.filter(
        fecha__gte=inicio_mes_anterior, 
        fecha__lt=inicio_mes_actual
    ).aggregate(total=Sum("monto"))["total"] or 0
    
    # Cálculo de variaciones
    variacion_gastos = ((gastos_mes_actual - gastos_mes_anterior) / gastos_mes_anterior * 100) if gastos_mes_anterior > 0 else 0
    variacion_ingresos = ((ingresos_mes_actual - ingresos_mes_anterior) / ingresos_mes_anterior * 100) if ingresos_mes_anterior > 0 else 0
    
    # Promedios diarios
    dias_transcurridos = (hoy - inicio_mes_actual).days + 1
    gastos_promedio_diario = gastos_mes_actual / dias_transcurridos if dias_transcurridos > 0 else 0
    ingresos_promedio_diario = ingresos_mes_actual / dias_transcurridos if dias_transcurridos > 0 else 0
    
    # Últimas transacciones
    gastos = Gasto.objects.order_by("-fecha")[:5]
    ingresos = Ingresos.objects.order_by("-fecha")[:5]
    
    # Colores para categorías
    colores = ["#ef4444", "#f97316", "#f59e0b", "#eab308", "#84cc16", "#22c55e", 
               "#10b981", "#14b8a6", "#06b6d4", "#0ea5e9", "#3b82f6", "#6366f1", 
               "#8b5cf6", "#a855f7", "#d946ef", "#ec4899", "#f43f5e"]
    
    # Distribución de gastos por categoría
    categorias_gastos = (
        Gasto.objects.values("categoria")
        .annotate(total=Sum("monto"))
        .order_by("-total")
    )
    total_gastos_categoria = sum(cat["total"] for cat in categorias_gastos)
    for i, cat in enumerate(categorias_gastos):
        cat["porcentaje"] = (
            round((cat["total"] / total_gastos_categoria) * 100, 2)
            if total_gastos_categoria > 0
            else 0
        )
        cat["color"] = colores[i % len(colores)]
    
    # Asignar colores a los gastos recientes
    colores_por_categoria = {cat["categoria"]: cat["color"] for cat in categorias_gastos}
    for gasto in gastos:
        gasto.color_categoria = colores_por_categoria.get(gasto.categoria, "#6b7280")
    
    # Distribución de ingresos por categoría (usando categoria en lugar de fuente)
    categorias_ingresos = (
        Ingresos.objects.values("categoria")
        .annotate(total=Sum("monto"))
        .order_by("-total")
    )
    total_ingresos_categoria = sum(cat["total"] for cat in categorias_ingresos)
    for i, cat in enumerate(categorias_ingresos):
        cat["porcentaje"] = (
            round((cat["total"] / total_ingresos_categoria) * 100, 2)
            if total_ingresos_categoria > 0
            else 0
        )
        cat["color"] = colores[(i + 5) % len(colores)]  # Desplazamos los colores para diferenciar
    
    # Asignar colores a los ingresos recientes
    colores_por_categoria_ingresos = {cat["categoria"]: cat["color"] for cat in categorias_ingresos}
    for ingreso in ingresos:
        ingreso.color_categoria = colores_por_categoria_ingresos.get(ingreso.categoria, "#6b7280")
    
    context = {
        "total_gastos": total_gastos,
        "total_ingresos": total_ingresos,
        "balance": balance,
        "gastos_count": gastos_count,
        "ingresos_count": ingresos_count,
        "tasa_ahorro": tasa_ahorro,
        "gastos_hoy": gastos_hoy,
        "gastos_semana": gastos_semana,
        "gastos_mes_actual": gastos_mes_actual,
        "gastos_mes_anterior": gastos_mes_anterior,
        "gastos_anio_actual": gastos_anio_actual,
        "ingresos_mes_actual": ingresos_mes_actual,
        "ingresos_mes_anterior": ingresos_mes_anterior,
        "variacion_gastos": variacion_gastos,
        "variacion_ingresos": variacion_ingresos,
        "gastos_promedio_diario": gastos_promedio_diario,
        "ingresos_promedio_diario": ingresos_promedio_diario,
        "gastos": gastos,
        "ingresos": ingresos,
        "categorias": categorias_gastos,
        "categorias_ingresos": categorias_ingresos,
    }
    return render(request, "index.html", context)
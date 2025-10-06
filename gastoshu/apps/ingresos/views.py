from django.shortcuts import render, redirect, get_object_or_404
from apps.ingresos.models import Ingresos
from apps.ingresos.forms import IngresoForm

# Create your views here.
def ingreso_list(request):
    ingresos = Ingresos.objects.all()
    return render(request, 'ingreso_list.html', {'ingresos': ingresos})

def ingreso_create(request):
    if request.method == 'POST':
        form = IngresoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingreso_list')
    else:
        form = IngresoForm()
    return render (request, 'ingreso_create.html', {'form': form})
        
def ingreso_update(request, pk):
    ingreso = get_object_or_404(Ingresos, pk=pk)
    if request.method == 'POST':
        form = IngresoForm(request.POST, instance=ingreso)
        if form.is_valid():
            form.save()
            return redirect('ingreso_list')
    else:
        form = IngresoForm(instance=ingreso)
    return render(request, 'ingreso_update.html', {'form': form, 'ingreso': ingreso})

def ingreso_delete(request, ingreso_id):
    ingreso = get_object_or_404(Ingresos, pk=ingreso_id)
    ingreso.delete()
    return redirect('ingreso_list')


from django.shortcuts import render, redirect, get_object_or_404
from .models import Gasto
from .form import GastoForm
from .models import Categoria  # Asegúrate de importar el modelo Categoria
def gasto_list(request):
    gastos = Gasto.objects.all()
    return render(request, 'gasto_list.html', {'gastos': gastos})

def gasto_create(request):
    if request.method == 'POST':
        form = GastoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gasto_list')
    else:
        form = GastoForm()
    return render(request, 'gasto_create.html', {'form': form})

def gasto_update(request, gasto_id):
    gasto = Gasto.objects.get(id=gasto_id)
    if request.method == 'POST':
        form = GastoForm(request.POST, instance=gasto)
        if form.is_valid():
            form.save()
            return redirect('gasto_list')
    else:
        form = GastoForm(instance=gasto)
    return render(request, 'gasto_create.html', {'form': form, 'titulo': 'Editar Gasto', 'boton': 'Guardar Cambios'})

def gasto_delete(request, gasto_id):
    gasto = get_object_or_404(Gasto, id=gasto_id)
    gasto.delete()
    return redirect('gasto_list')

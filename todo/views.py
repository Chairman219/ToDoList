from itertools import takewhile

from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm

# Zobrazení všech úkolů
def task_list(request):
    sort_by = request.GET.get('sort_by', 'date')

    if sort_by == "status":
        tasks = Task.objects.all().order_by('completed', '-created_at') # Seřazení podle statusu (nevyřízené první)
    else:
        tasks = Task.objects.all().order_by('-created_at') # Seřazení podle data (nejnovější první)

    return render(request, 'todo/task_list.html', {'tasks': tasks})

# Přidání nového úkolu
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'todo/add_task.html', {'form': form})

# Označení úkolu jako doknčeného
def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = True
    task.save()
    return redirect('task_list')

# Smazání úkolu
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('task_list')
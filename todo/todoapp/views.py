from django.http import *
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import *
from . forms import *
from django.views.generic import *

class TaskList(ListView):
    model = Task
    template_name = 'index.html'
    context_object_name = 'task_collection'

class TaskDetailView(DetailView):
    model = Task
    template_name = 'details.html'
    context_object_name = 'task_collection'


class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'update.html'
    context_object_name = 'task'
    fields = ('name', 'priority', 'date')

    def get_success_url(self):
        return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('cbvhome')

# Create your views here.
def index(request):
    task_collection = Task.objects.all()

    if request.method == 'POST' and request.POST.get('task', '') is not None:
        name = request.POST.get('task', '')
        priority = request.POST.get('priority', '')
        date = request.POST.get('datecompletion','')

        task = Task(name=name, priority=priority, date=date)
        task.save()

    return render(request, 'index.html', {'task_collection': task_collection})


# def details(request):
#     task = Task.objects.all()
#     return render(request, 'details.html', {'task': task})

def delete(request, taskid):
    task = Task.objects.get(id=taskid)
    if request.method == 'POST':
        task.delete()
        return redirect('/')

    return render(request, 'delete.html')

def update(request, taskid):
    task = Task.objects.get(id=taskid)
    form = UpdateForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('/')

    return render(request, 'edit.html', {'form':form, 'task':task})

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Task
from .models import Task
from .forms import TaskForm

def task_list(request):
    """ View to display all tasks in a list view """
    tasks = Task.objects.all().order_by('-id')  # Show latest tasks first
    form = TaskForm()
    return render(request, 'todo/task_list.html', {'tasks': tasks, 'form': form})

def task_create(request):
    """ AJAX view to create a new task """
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            return JsonResponse({
                'message': 'Task created successfully!',
                'task': {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'status': task.status,
                    'due_date': task.due_date.strftime('%Y-%m-%d'),
                    'priority': task.priority
                }
            })
        else:
            return JsonResponse({'error': form.errors}, status=400)


def get_tasks(request):
    """ AJAX view to return "To-Do" and "In Progress" tasks """
    tasks = Task.objects.filter(status__in=["To-Do", "In Progress"]).order_by('-id')
    task_list = [
        {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'due_date': task.due_date.strftime('%Y-%m-%d'),
            'priority': task.priority
        }
        for task in tasks
    ]
    return JsonResponse({'tasks': task_list})


def mark_task_done(request, task_id):
    """ AJAX function to mark task as Done """
    task = get_object_or_404(Task, id=task_id)
    if task.status in ["To-Do", "In Progress"]:  # Change status only if it's not already "Done"
        task.status = "Done"
        task.save()
        return JsonResponse({'message': 'Task marked as done!', 'task_id': task.id, 'new_status': 'Done'})
    return JsonResponse({'error': 'Task already marked as done!'})



def task_delete(request, task_id):
    """ AJAX view to delete a task """
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return JsonResponse({'message': 'Task deleted successfully!', 'task_id': task_id})


def show_tasks(request):
    """ View for showing ongoing tasks """
    return render(request, 'todo/show_tasks.html')

def task_edit(request, task_id):
    """ Update task details """
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        task.title = request.POST.get("title", task.title)
        task.description = request.POST.get("description", task.description)
        task.due_date = request.POST.get("due_date", task.due_date)
        task.priority = request.POST.get("priority", task.priority)
        task.save()
        return redirect('show_tasks')  # Redirect back to the ongoing tasks page
    return render(request, 'todo/edit_task.html', {'task': task})

def edit_task_page(request, task_id):
    """ Render the Edit Task page """
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'todo/edit_task.html', {'task': task})
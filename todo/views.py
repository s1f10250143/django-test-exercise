from django.shortcuts import render
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from todo.models import Task
from django.http import Http404


def index(request):
    if request.method == 'POST':
        task = Task(
            title=request.POST['title'],
            due_at=make_aware(parse_datetime(request.POST['due_at']))
        )
        task.save()

    if request.GET.get('order') == 'due':
        tasks = Task.objects.order_by('due_at')
    else:
        tasks = Task.objects.order_by('-posted_at')

    context = {
        'tasks': tasks
    }

    return render(request, 'todo/index.html', context)

def test_index_get_order_post(self):
    task1 = Task(title='task1', due_at=timezone.make_aware(datetime(2024, 7, 1)))
    task1.save()

    task2 = Task(title='task2', due_at=timezone.make_aware(datetime(2024, 8, 1)))
    task2.save()

    client = Client()
    response = client.get('/?order=post')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.templates[0].name, 'todo/index.html')
    self.assertEqual(response.context['tasks'][0], task2)
    self.assertEqual(response.context['tasks'][1], task1)

def test_index_get_order_due(self):
    task1 = Task(title='task1', due_at=timezone.make_aware(datetime(2024, 7, 1)))
    task1.save()

    task2 = Task(title='task2', due_at=timezone.make_aware(datetime(2024, 8, 1)))
    task2.save()

    client = Client()
    response = client.get('/?order=due')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.templates[0].name, 'todo/index.html')
    self.assertEqual(response.context['tasks'][0], task1)
    self.assertEqual(response.context['tasks'][1], task2)
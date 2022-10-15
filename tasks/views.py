
from django.shortcuts import  render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from . forms import Taskform
from . models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


#from django.http import HttpResponse

# METODOS
# GET - mi compu =>  pide datos al servidor (menos seguro)
# POST - mi compu => envia datos al servidort(mas seguro)


# Create your views here.

def home(request):
    return render(request, 'home.html')


def home(request):
    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # register user
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
                
            except:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': "el usuario ya existe"
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': "contraseñas no coinciden"
        })

       
        
@login_required
def tasks(request):
    task = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': task})

@login_required
def tasks_completed(request):
    task = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks': task})


@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
        'form': Taskform

        })

    else:
        try:
            form =Taskform(request.POST)
            new_task =form.save(commit=False)
            new_task.user=request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': Taskform,
                'error': 'por favor poner un dato valido'

        })
    




@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task , pk=task_id , user=request.user)
        form =Taskform(instance=task)
        return render(request, 'task_detail.html' , {'task':task, 'form': form})

    else:
        try:
            task=  get_object_or_404(Task, pk=task_id, user=request.user)
            form=  Taskform(request.POST, instance=task)
            form.save()
            return redirect('tasks')
            #return render(request, 'task_detail.html' , {'task':task, 'form': form})
        except ValueError:
              return render(request, 'task_detail.html' , {'task':task, 'form': form,
              'error': 'Error actualizando tarea'})

@login_required
def complete_task(request, task_id):
    task=get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method=='POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')



@login_required
def delate_task(request, task_id):
    task=get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method=='POST':
        task.delete()
        return redirect('tasks')






@login_required
def logoutFun(request):
    logout(request)
    return redirect('home')




def loginFun(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
        'form': AuthenticationForm })
    else:

      user =  authenticate(request, username=request.POST['username'], password=request.POST['password']) 
      if user is None:
         return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': 'usuario o contraseña incorrecta'
            
        })

      else:
        login(request,user)
        return redirect('tasks')

    




       








  #  return render(request, 'signin.html', {
 #       'form': AuthenticationForm
#    })

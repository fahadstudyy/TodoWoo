from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import todo
from django.utils import timezone


def home(request):
    return render(request,'todo/home.html')


def signups(request):
    if request.method == 'GET': 
        return render(request,'todo/signupuser.html', {'form': UserCreationForm})
    else:
        try:
            if request.POST['password1'] == request.POST['password2']:    
                user = User.objects.create_user(username = request.POST['username'],password = request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')

        except IntegrityError:
            return render(request,'todo/signupuser.html', {'form': UserCreationForm,'exist': 'The user You Enter Already Exist'})
                
        else:
            return render(request,'todo/signupuser.html', {'form': UserCreationForm,'mismatch': 'Password mismatch.'})

def loginuser(request):
    if request.method == 'GET':
        return render(request,'todo/loginuser.html',{'form': AuthenticationForm })
    else:
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            return render(request,'todo/loginuser.html',{'form': AuthenticationForm, 'error':'Username or password does not match' })
        else:
            login(request, user)
            return redirect('currenttodos')

def currenttodos(request):
    todos = todo.objects.filter(user = request.user, datecompleted__isnull = True)
    return render(request,'todo/currenttodos.html', {'todos': todos})

def completetodos(request):
    todos = todo.objects.filter(user = request.user, datecompleted__isnull = False).order_by('-datecompleted')
    return render(request,'todo/completedtodos.html', {'todos': todos})

def viewtodo(request, todo_pk):
    todos = get_object_or_404(todo, pk=todo_pk)
    if request.method == 'GET':
        form = TodoForm(instance=todos)
        return render(request,'todo/viewtodo.html', {'todos': todos, 'form': form})
    else:
        try:
             form = TodoForm(request.POST, instance=todos)
             form.save()
             return redirect('currenttodos')
        except ValueError:
            return render(request,'todo/viewtodo.html', {'form': TodoForm(), 'error': 'Bad Data'}) 
  
def todos(request):
    if request.method == 'GET':
        return render(request,'todo/createtodo.html', {'form': TodoForm()})
    else: 
        try:    
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except  ValueError:
            return render(request,'todo/createtodo.html', {'form': TodoForm(), 'error': 'Data Increased Limit'})


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    


def completetodo(request, todo_pk):
    todos = get_object_or_404(todo, pk=todo_pk, user = request.user)
    if request.method == 'POST':
        todos.datecompleted  = timezone.now()
        todos.save()
        return redirect('currenttodos')


def deletetodo(request, todo_pk):
    todos = get_object_or_404(todo, pk=todo_pk, user = request.user)
    if request.method == 'POST':
        todos.delete()
        return redirect('currenttodos')

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login as LoginUser,logout 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from todoapp.form import TODOForm
from todoapp.models import TODO
from django.contrib.auth.decorators import login_required

# Create your views here.


def welcome(request):
    return render(request,"welcome.html")

@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        todos = TODO.objects.filter(user=user).order_by('priority')
        return render(request,"index.html",context ={'form':form,'todos': todos})


def login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        context = {
            "form" : form
        }
        return render(request,"login.html",context=context)
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
           username= form.cleaned_data.get('username')
           password = form.cleaned_data.get('password')
           user=authenticate(username=username, password = password)
           if user is not None:
               LoginUser(request,user)
               return redirect('home')
        else:
            context = {
            "form" : form
            }
            return render(request,"login.html",context=context)


def sinup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        context = {
            "form" : form
        }
        return render(request,"sinup.html", context = context)
    else:
        form = UserCreationForm(request.POST)
        context = {
            "form" : form
        }
        if form.is_valid():
            user = form.save()
            if user is not None:
                
                return redirect('login')
        else:
            
           return render(request,"sinup.html", context = context)
        


@login_required(login_url='login')
def add_todo(request):
    if request.user .is_authenticated:
        user = request.user
        form = TODOForm(request.POST)
        if form.is_valid():
           todo = form.save(commit=False)
           todo.user = user
           todo.save()

           return redirect("home")
        else:
            return render(request,"sinup.html", context = {'form':form})
        

@login_required(login_url='login')
def signout(request):
      logout(request)
      return redirect('welcome')

       

def delete_todo(request,id):
    TODO.objects.get(pk = id).delete()
    return redirect("home")




def change_todo(request,id,status):
    todo = TODO.objects.get(pk = id)
    todo.status = status 
    todo.save()
    return redirect('home')

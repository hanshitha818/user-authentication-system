##use following link 
##https://medium.com/@prathamanchan22/send-text-message-sms-in-python-using-fast2sms-a1399e863552

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .FACE_DETECTION import save_image
from .Face_Recognitions import face_id
import requests
import EMAIL
import random

def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.create_user(request.POST['username'], password=request.POST['password1'],email=request.POST['phone'])

                    FD = save_image(request.POST['username'])
                    if(FD == 1):                
                        user.save()
                        login(request, user)
                        return redirect('loginuser')
                    else:
                        return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Connect camera properly'})

                except IntegrityError:
                    return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            phone_num = request.user.email
            print(phone_num)
            OTP = random.randint(1111,9999)
            send_otp = 1        # set to zero if do not want to send SMS
            EMAIL.send_mail("OTP of your Secured Login system is : " + str(OTP) ,phone_num)
            
            # if(send_otp == 1):
            #     url = "https://www.fast2sms.com/dev/bulk"
                
            #     payload = "sender_id=FSTSMS&message= OTP for system" + str(OTP) + "&language=english&route=p&numbers=9890993809," + str(phone_num) 
    
            #     headers = {
            #     'authorization': "0X26WLpVr9YMgkSIh37qBd4btmaFnxuj1Zi8CTzUHlJQOwfsvcs3CRJL5mbAd9wOBKrN16SXfZogtu28",
            #     'Content-Type': "application/x-www-form-urlencoded",
            #     'Cache-Control': "no-cache",
            #     }

            #     response = requests.request("POST", url, data=payload, headers=headers)
            #     print(response.text)

            print(OTP)
            f = open("generated_otp.txt", "w")
            f.write(str(OTP))
            f.close()
            return redirect('currenttodos')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form':TodoForm(), 'error':'Bad data passed in. Try again.'})

@login_required
def currenttodos(request):
    if request.method == 'GET':
        try:
            otp =request.GET['otp']
            print(otp)
            f = open("generated_otp.txt", "r")
            entered_otp = f.read()
            if(str(entered_otp) == str(otp)):
                print('OTP MATCHED')
                # return redirect('currenttodos')
                return redirect('completedtodos')
                # return render(request, 'todo/viewtodo.html')
                # viewtodo()

            else:
                print("ENTERED WRONG OTP")
                return render(request, 'todo/currenttodos.html',{'error':'Wrong OTP'})
        except:
            pass
    return render(request, 'todo/currenttodos.html')

@login_required
def completedtodos(request):
    print('SNIST')
    print(request.user.username)
    FR = face_id(request.user.username)    
    if FR == 0:
        logout(request)
        return redirect('home')
    return render(request, 'todo/completedtodos.html')

@login_required
def viewtodo(request):
    print('SNIST')
    return render(request, 'todo/viewtodo.html')


    # todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    # if request.method == 'GET':
    #     form = TodoForm(instance=todo)
    #     return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form})
    # else:
    #     try:
    #         form = TodoForm(request.POST, instance=todo)
    #         form.save()
    #         return redirect('currenttodos')
    #     except ValueError:
    #         return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form, 'error':'Bad info'})

@login_required
def completetodo(request):
    print('SNIST')
    # todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    # if request.method == 'POST':
    #     todo.datecompleted = timezone.now()
    #     todo.save()
    return redirect('completedtodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

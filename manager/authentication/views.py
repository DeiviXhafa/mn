from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
class RegisterView(View):
    def get(self,request):
        if request.user.is_anonymous:
            return render(request,'register.html')
        else:
            return redirect('/')
    def post(self,request):
        if request.user.is_anonymous:
            post_data=request.POST
            username=post_data['username']
            password=post_data['password']
            confirm_password=post_data['confirm_password']
            if password==confirm_password:
                User.objects.create_user(username=username,password=password)
                return redirect('/authentication/login')
        else:
            return redirect('/')
class LoginView(View):
    def get(self,request):
        if request.user.is_anonymous:
            return render(request,'login.html')
        else:
            return redirect('/')
    def post(self,request):
        if request.user.is_anonymous:
            post_data=request.POST
            username=post_data['username']
            password=post_data['password']
            user=authenticate(username=username,password=password)
            if user:
                login(request,user)
                if user.is_superuser:
                    return redirect('/admin')
                return redirect('/project/project/')
        else:
            return redirect('/')
class LogoutView(View):
    def get(self,request):
        if request.user.is_anonymous:
            return redirect('/')
        else:
            logout(request)
            return redirect('/authentication/login')

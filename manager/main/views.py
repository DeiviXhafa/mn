from django.shortcuts import render,redirect
from django.views import View
from project.models import *
class HomeView(View):
    def get(self,request):
        return redirect('/project/project/')

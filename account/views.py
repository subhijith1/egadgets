from django.shortcuts import render,redirect
from django.views.generic import View,CreateView,FormView,TemplateView,ListView
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.forms.models import BaseModelForm
from django.urls import reverse_lazy
from .models import Product
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

# Create your views here.

def signin_requried(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.error(request,'Login Required.....')
            return redirect('log')
    return inner

dec=[signin_requried,never_cache]





# class Logview(View):
    # def get(self,request):
    #     form=Logform()
    #     return render(request,'log.html',{"form":form})
    # def post(self,request):
    #     form_data=Logform(data=request.POST)
    #     if form_data.is_valid():
    #         uname=form_data.cleaned_data.get('username')
    #         pswd=form_data.cleaned_data.get('password')
    #         user=authenticate(request,username=uname,password=pswd)
    #         if user:
    #             messages.success(request,"Login Successfull")
    #             return redirect('home')
    #         else:
    #             messages.error(request,"Invalid Username Or Password")
    #             return redirect('log')
    #     return render(request,'log.html',{"form":form_data})

class Logview(FormView):
    template_name="log.html"
    form_class=Logform
    def post(self,request):
        form_data=Logform(data=request.POST)
        if form_data.is_valid():
            uname=form_data.cleaned_data.get('username')
            pswd=form_data.cleaned_data.get('password')
            user=authenticate(request,username=uname,password=pswd)
            if user:
                login(request,user)
                messages.success(request,"Login Successfull")
                return redirect('home')
            else:
                messages.error(request,"Invalid Username Or Password")
                return redirect('log')
        return render(request,'log.html',{"form":form_data})

# class Regview(View):
    # def get(self,request):
    #     form=Regform()
    #     return render(request,'reg.html',{"form":form})
    # def post(self,request):
    #     form_data=Regform(data=request.POST)
    #     if form_data.is_valid():
    #         form_data.save()
    #         messages.success(request,"Registration Successfull")
    #         return redirect('log')
    #     messages.error(request,"Validation Failed")
    #     return render(request,'reg.html',{"form":form_data})

class Regview(CreateView):
    template_name="reg.html"
    form_class=Regform
    model=User
    success_url=reverse_lazy("log")
    def form_valid(self, form):
        messages.success(self.request,"registration succesfull....")
        return super().form_valid(form)
    def form_invalid(self,form):
        messages.error(self.request,"registration failed....")
        return super().form_invalid(form)

# class Homeview(View):
    # def get(self,request):
    #     return render(request,"home.html")

# class Homeview(TemplateView):
#     template_name="home.html"
@method_decorator(dec,name='dispatch')
class Homeview(ListView):
    template_name="home.html"
    queryset=Product.objects.all()
    context_object_name="data"

class Lgoutview(View):
    def get(self,request):
        logout(request)
        return redirect('log')
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import render,redirect
from .forms import RegisterForm
def register(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save();login(request,user);messages.success(request,'Account created.');return redirect('home')
    else:form=RegisterForm()
    return render(request,'accounts/register.html',{'form':form})
class LocalLoginView(LoginView):template_name='accounts/login.html'

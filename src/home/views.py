from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout

# Create your views here.
def index(request):
    return render(request, 'home/index.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('bill_group:index')

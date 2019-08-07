from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request,'index.html')
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    err_info = {}
    print(username," : ",password)
    if username.strip() == 'Jack':
        err_info['username'] = '用户名'
    elif password.strip() == 'Rose':
        err_info['password'] = '密码'

    return render(request,'index.html',{'err_info':err_info})

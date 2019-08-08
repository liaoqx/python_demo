# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from CA_Demo.models import EmployeesInfo
import hashlib
# Create your myviews here.
#存放系统公共部分的view
def login(request):
    if request.session.get('userid') is not None: #若已经登录则不用再次登录
        return HttpResponseRedirect('show_main')

    userid = request.POST.get('userid')
    password = request.POST.get('password')
    err_info = ""
    if userid is None or password is None or userid.strip() == "" or password.strip() == "":
        err_info = "用户名或密码不能为空"
    elif len(userid.strip()) < 2 or len(password.strip()) < 6 or len(password.strip()) > 16:
        err_info = "用户名或密码(6-16位)格式错误"
    else:
        try:
            emp = EmployeesInfo.objects.get(emp_id=userid)
        except EmployeesInfo.DoesNotExist:
            emp = None
        if emp:
            md5 = hashlib.md5()
            md5.update(password.encode('utf-8'))
            if md5.hexdigest() == emp.password:
                request.session['userid'] = emp.emp_id  #保存session
                request.session['username'] = emp.emp_name
                return HttpResponseRedirect('show_main')
        err_info = '用户名或密码错误'
    return render(request,'index.html',{'err_info':err_info,
                                        'userid':userid,
                                        'password':password})
def exit(request):
    request.session.flush()
    resp_html = """<html><body onLoad='window.open("show_index","_top")'></body></html>"""
    return HttpResponse(resp_html,content_type='text/html')


def return_html(request,html_name):
    '''根据参数跳转到相应名字的页面'''
    if html_name == 'main':
        if request.session.get('userid') is None: #若session值为空 => 未登录 => 进入登录页面
            return HttpResponseRedirect('show_index')
        return render(request,'main.html',{'userid':request.session.get('userid'),
                                           'username':request.session.get('username')})
    return render(request,"{html_name}.html".format(html_name = html_name))

# def content_manage(request,func,method):
#     '''跳转到func模块下method.html管理页面上'''
#     return render(request,'{func}/{method}.html'.format(func = func,method = method))
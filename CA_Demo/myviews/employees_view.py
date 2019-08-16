#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from ..models import EmployeesInfo,RepairInfo
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
import logging;logging.basicConfig(level=logging.INFO)
from django.db.models import Q
import hashlib
from .tools import paging
import json

dept_name_dict = {"ED01":u"人力资源部","ED02":u"财务部","ED03":u"运维部","ED04":u"研发部","ED05":u"质量监察部","ED06":u"营销部"}
kw = None

def translateDept(employee_list):
    '''将部门编号转换为部门名称,转换日期格式'''
    for pos,employee in enumerate(employee_list):
        dept_id = employee['emp_dept']
        dept_name = dept_name_dict[dept_id]
        employee_list[pos]['emp_dept'] = dept_name
        employee_list[pos]['join_time'] = employee['join_time'].strftime("%Y-%m-%d")
    return employee_list


def getRequestEmpData(request):
    '''获取添加/修改员工页面的员工信息'''
    password = ""
    id = request.POST.get("id")
    emp_id = request.POST.get("emp_id")
    emp_name = request.POST.get("emp_name")
    telephone = request.POST.get("telephone")
    email = request.POST.get("email")
    sex = request.POST.get("sex")
    join_time = request.POST.get("join_time")
    emp_dept = request.POST.get("emp_dept")
    is_removed = request.POST.get("is_removed")

    is_admin = request.POST.get("is_admin")
    if is_admin is not None and is_admin == 'T':
        password = request.POST.get("password")

    employee = EmployeesInfo(id = id,emp_id = emp_id,emp_name = emp_name,telephone = telephone,
                             email = email,sex = sex,join_time = join_time,emp_dept = emp_dept,is_removed = is_removed,is_admin = is_admin,password = password)
    return employee

def getAllEmployees(request):
    '''获取所有员工信息'''
    cur_page = request.GET.get("page")
    employee_list = EmployeesInfo.objects.all().order_by("id")\
                                            .values('id','emp_id','emp_name','is_admin','telephone','email','sex','join_time','emp_dept','is_removed')
    employees = translateDept(employee_list)
    #logging.info("employees:{0}".format(employees))

    cur_employee_list,page_num,cur_page,previous_page,next_page = paging(employees,cur_page)

    return render(request,'employees/manage_employees.html',{"employee_list":cur_employee_list,
                                                             "page_num":range(1,page_num + 1),
                                                             "cur_page":cur_page,
                                                             "previous_page":previous_page,
                                                             "next_page":next_page,
                                                             "url":"manageEmployees"})


def addEmployee(request):
    '''添加员工'''
    employee = getRequestEmpData(request)
    employee.save()
    return HttpResponseRedirect('manageEmployees')

def getEmployeesByIdOrName(request):
    '''通过id,name查询员工'''
    keywords = request.GET.get("keywords")
    cur_page = request.GET.get("page")
    global kw
    if keywords is None and kw is None:
        return HttpResponseRedirect("manageEmployees")

    elif keywords is not None:
        kw = keywords

    employee_list = EmployeesInfo.objects.filter(Q(emp_id__icontains=kw)
                                                 | Q(emp_name__icontains=kw) | Q(emp_dept__icontains=kw)).order_by("id")\
                                                .values('id','emp_id','emp_name','is_admin','telephone','email','sex','join_time','emp_dept','is_removed')
    employees = translateDept(employee_list)
    #logging.info("employee_list:{0}".format(employees))

    cur_employee_list, page_num, cur_page, previous_page, next_page = paging(employees, cur_page)

    return render(request, 'employees/manage_employees.html', {"employee_list": cur_employee_list,
                                                               "page_num": range(1, page_num + 1),
                                                               "cur_page": cur_page,
                                                               "previous_page": previous_page,
                                                               "next_page": next_page,
                                                               "url": "getEmployeesByIdOrName"})


def updateEmployeeById(request):
    '''通过员工编号修改员工信息'''
    old_id = request.POST.get("old_id")
    emp = getRequestEmpData(request)
    EmployeesInfo.objects.filter(id=old_id).update(id=emp.id,emp_id = emp.emp_id,emp_name = emp.emp_name,telephone = emp.telephone,
                                                email = emp.email,sex = emp.sex,join_time = emp.join_time,emp_dept = emp.emp_dept,is_removed = emp.is_removed)

    return HttpResponseRedirect('manageEmployees')

def updateAdminRight(request):
    '''修改员工权限'''
    if request.method == "GET":
        '''取消员工的管理权限'''
        emp_id = request.GET.get("emp_id")
        EmployeesInfo.objects.filter(emp_id=emp_id,is_removed='F',is_admin='T').update(is_admin='F',password = "")
    elif request.method == "POST":
        '''将员工设置为管理员用户'''
        emp_id = request.POST.get('emp_id')
        password = request.POST.get('password')
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        pwd_md5 = md5.hexdigest()
        #logging.info("pwd_md5:{0}".format(pwd_md5))
        EmployeesInfo.objects.filter(emp_id = emp_id,is_removed='F',is_admin='F').update(is_admin='T',password=pwd_md5)
    return HttpResponseRedirect('manageEmployees')

def getDeptInfo(): #将部门信息封装为一个字典数组
    depts = []
    for dept_key in dept_name_dict:
        dept = {'dept_id': dept_key, 'dept_name': dept_name_dict[dept_key]}
        depts.append(dept)
    return depts

def deleteEmployeeById(request):
    '''根据员工编号删除员工'''
    ids = request.GET.get("emp_id")
    ids_list = []
    for id in ids.split(","):
        ids_list.append(id)

    ids_in_repair = RepairInfo.objects.filter(employee_id__in=ids_list).values("employee_id").distinct()
    ids_in_repair_list = []
    for id in ids_in_repair:
        ids_in_repair_list.append(id['employee_id'])
        ids_list.remove(id['employee_id'])

    EmployeesInfo.objects.filter(id__in=ids_in_repair_list).update(is_removed='T')
    EmployeesInfo.objects.filter(id__in=ids_list).delete()
    return HttpResponseRedirect("manageEmployees")


def updateAdminPwd(request):
    '''修改管理员密码'''
    oldPwd = request.POST.get("oldPwd")
    newPwd = request.POST.get("newPwd")
    emp_id = request.POST.get("emp_id")

    #logging.info("oldPwd:{0} -- newPwd:{1} -- emp_id:{2}".format(oldPwd,newPwd,emp_id))
    md5_old_pwd = hashlib.md5()
    md5_old_pwd.update(oldPwd.encode('utf-8'))

    try:
        EmployeesInfo.objects.get(emp_id=emp_id, password=md5_old_pwd.hexdigest())
    except EmployeesInfo.DoesNotExist:
        err_info = u"旧密码错误"
        return HttpResponse(json.dumps({'statusCode':-1,'err_info':err_info},ensure_ascii=False),content_type="application/json;charset=utf8")
    else:
        md5_new_pwd = hashlib.md5()
        md5_new_pwd.update(newPwd.encode("utf-8"))
        EmployeesInfo.objects.filter(emp_id = emp_id).update(password=md5_new_pwd.hexdigest())
        return HttpResponse(json.dumps({'statusCode':0},ensure_ascii=False),content_type="application/json;charset=utf8")

def employeesFunc(request,emp_func):
    if emp_func == "manageEmployees":
        return getAllEmployees(request)

    elif emp_func == "getEmployeesByIdOrName":
        return getEmployeesByIdOrName(request)

    elif emp_func == "toUpdateEmployeeById":
        id = request.GET.get("id")
        employee = EmployeesInfo.objects.get(id = id)
        employee.join_time = employee.join_time.strftime("%Y-%m-%d")
        depts = getDeptInfo()
        return render(request,'employees/updateEmployee.html',{'employee':employee,'depts':depts})

    elif emp_func == "updateEmployeeById":
        return updateEmployeeById(request)

    elif emp_func == "toAddEmployee":
        depts = getDeptInfo()
        return render(request,'employees/addEmployee.html',{'depts':depts})

    elif emp_func == "addEmployee":
        return addEmployee(request)

    elif emp_func == "updateAdminRight":
        return updateAdminRight(request)

    elif emp_func == "deleteEmployeeById":
        return deleteEmployeeById(request)

    elif emp_func == "updateAdminPwd":
        return updateAdminPwd(request)


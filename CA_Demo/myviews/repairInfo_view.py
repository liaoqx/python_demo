import datetime
import traceback
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from ..models import RepairInfo, CustomersInfo, CarsInfo, EmployeesInfo, UserCarsInfo

from .tools import paging

def zipRepairInfosData(rep_list):
    '''根据客户信息查询客户的车辆信息,并组装成一个列表返回'''
    infos = []
    # logging.info("customer_list:{0}".format(customer_list))
    for rep in rep_list:
        Infos = {}
        Infos['id'] = rep.id
        Infos['repair_desc'] = rep.repair_desc
        Infos['repair_time'] = rep.repair_time
        Infos['plate_number'] = rep.plate_number
        # 通过RepairInfo反向查询EmployeesInfo
        employee = rep.employee
        # print(employee.emp_name,employee.id)
        Infos['emp_id'] = employee.emp_id
        Infos['emp_name'] = employee.emp_name
        # 通过RepairInfo反向查询CustomersInfo
        customer = rep.customer
        # print(customer.cus_name, customer.telephone, customer.email)
        Infos['cus_name'] = customer.cus_name
        Infos['telephone'] = customer.telephone
        Infos['email'] = customer.email
        infos.append(Infos)
    return infos


def getAllRepairInfos(request):
    #查询所有RepairInfo
    cur_page = request.GET.get("page")
    rep_list = RepairInfo.objects.all() #QuerySet
    infos=zipRepairInfosData(rep_list)
    cur_rep_list, page_num, cur_page, previous_page, next_page = paging(infos, cur_page)
    return render(request, 'repairInfos/manage_repairInfos.html', {"infos":cur_rep_list,
                                                   "page_num":range(1,page_num + 1),
                                                   "cur_page":cur_page,
                                                   "previous_page":previous_page,
                                                   "next_page":next_page,
                                                   "url":"manageRepairInfos"})

def getRepairInfosByEmp(request):
    #根据员工的编号或姓名查询维修记录
    keywords = request.GET.get("keywords")
    #先根据员工编号获取员工的id
    emp_list = EmployeesInfo.objects.filter(Q(emp_id=keywords) | Q(emp_name=keywords))
    id=emp_list[0].id
    #再通过员工的ID查询维修记录
    rep_list=RepairInfo.objects.filter(employee_id=id)
    infos = zipRepairInfosData(rep_list)
    return render(request, 'repairInfos/manage_repairInfos.html', {"infos": infos})


def getEmployees():
    '''获取所有员工信息'''
    employees = EmployeesInfo.objects.filter(is_removed='F')
    return employees
def getCustomers():
    '''获取所有顾客信息'''
    customers = CustomersInfo.objects.all()
    return customers

def addRepairInfo(request):
    '''添加维修信息'''
    repair= RepairInfo()
    repair.customer_id=request.POST.get('customer')
    repair.employee_id=request.POST.get('employee')
    repair.plate_number=request.POST.get('plate_number')
    repair.repair_desc=request.POST.get('repair_desc')
    repair.repair_time=datetime.datetime.now()
    repair.save()
    return HttpResponseRedirect('manageRepairInfos')

def deleteRepairInfoById(request):
    '''删除维修信息'''
    ids = request.GET.get("id")
    ids_list = []
    for id in ids.split(","): #构造由待删除记录id编号组成的数组
        ids_list.append(id)
    #logging.info("deleteErrors' ids:<{0}>; ids_list:<{1}>".format(ids,ids_list))
    RepairInfo.objects.filter(id__in=ids_list).delete()  #批量删除数据
    return HttpResponseRedirect('manageRepairInfos')

def updateRepairInfoById(request):
    '''修改维修信息'''
    oldId = request.GET.get("oldId")
    customer = request.POST.get("customer")
    employee = request.POST.get("employee")
    plate_number = request.POST.get("plate_number")
    repair_desc = request.POST.get("repair_desc")
    RepairInfo.objects.filter(id=oldId).update(customer=customer,employee=employee,plate_number=plate_number,repair_desc=repair_desc)
    return HttpResponseRedirect('manageRepairInfos')

def repairInfoFunc(request,rep_func):
    '''根据传入参数调用不同的处理方法'''
    if rep_func == "manageRepairInfos":
        return getAllRepairInfos(request)

    elif rep_func == "toAddRepairInfo":
        return render(request, 'repairInfos/addRepairInfo.html', {"employees": getEmployees(),"customers":getCustomers()})

    elif rep_func == "addRepairInfo":
        return addRepairInfo(request)

    elif rep_func == "toUpdateRepairInfoById":
        repair_id = request.GET.get("id")
        repair = RepairInfo.objects.get(id=repair_id)
        return render(request, 'repairInfos/updateRepairInfo.html', {'repair': repair,"employees": getEmployees(),"customers":getCustomers()})

    elif rep_func == "updateRepairInfoById":
        return updateRepairInfoById(request)

    elif rep_func == "getRepairInfosByEmp":
        return getRepairInfosByEmp(request)

    elif rep_func == "deleteRepairInfoById":
        return deleteRepairInfoById(request);


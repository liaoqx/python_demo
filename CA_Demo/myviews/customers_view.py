# _*_ coding=utf-8 _*_
import logging;logging.basicConfig(level=logging.INFO)
import traceback
from ..models import CustomersInfo,UserCarsInfo
from django.db.models import Q
from django.shortcuts import render

def zipCustomersData(customer_list):
    '''根据客户信息查询客户的车辆信息,并组装成一个列表返回'''
    users = []
    # logging.info("customer_list:{0}".format(customer_list))
    for customer in customer_list:
        user = {}
        #car_list = customer.usercarsinfo_set.all()
        car_list = UserCarsInfo.objects.filter(customer_id = customer['id'])
        user['customer'] = customer
        user['car_list'] = car_list
        users.append(user)
    return users

def getAllCustomers(request):
    '''获取所有客户信息(id,cus_name,telephone,email,sex,birthday)'''
    customer_list = CustomersInfo.objects.all().values('id','cus_name','telephone','email','sex','birthday')
    users = zipCustomersData(customer_list)
    return render(request,'customers/manage_customers.html',{
        "users":users
    })

def getCustomersByIdOrName(request):
    '''通过客户id或姓名的方式查询客户信息'''
    keywords = request.GET.get("keywords")
    customer_list = CustomersInfo.objects.filter(Q(id__icontains=keywords) | Q(cus_name__icontains=keywords)).values('id','cus_name','telephone','email','sex','birthday')
    users = zipCustomersData(customer_list)
    return render(request, 'customers/manage_customers.html', {
        "users": users
    })

def customerFunc(request,cus_func):
    '''根据传入参数调用不同的处理方法'''
    if cus_func == "manageCustomers":
        return getAllCustomers(request)

    elif cus_func == "getCustomersByIdOrName":
        return getCustomersByIdOrName(request)

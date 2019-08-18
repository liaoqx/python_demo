#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import logging;logging.basicConfig(level=logging.INFO)
import traceback
from ..models import CustomersInfo,UserCarsInfo
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .tools import paging

kw = None

def zipCustomersData(customer_list):
    '''根据客户信息查询客户的车辆信息,并组装成一个列表返回'''
    users = []
    # logging.info("customer_list:{0}".format(customer_list))
    for customer in customer_list:
        user = {}
        #car_list = customer.usercarsinfo_set.all()
        car_list = UserCarsInfo.objects.filter(customer_id = customer['id'])
        customer['birthday'] = customer['birthday'].strftime("%Y-%m-%d")
        user['customer'] = customer
        user['car_list'] = car_list
        users.append(user)
    return users

def getAllCustomers(request):
    '''获取所有客户信息(id,cus_name,telephone,email,sex,birthday)'''
    customer_list = CustomersInfo.objects.all().order_by("id").values('id','cus_name','telephone','email','sex','birthday')
    users = zipCustomersData(customer_list)

    cur_page = request.GET.get("page")
    cur_user_list,page_num,cur_page,previous_page,next_page = paging(users,cur_page)

    return render(request,'customers/manage_customers.html',{ "users":cur_user_list,
                                                              "page_num":range(1,page_num + 1),
                                                              "cur_page":cur_page,
                                                              "previous_page":previous_page,
                                                              "next_page":next_page,
                                                              "url":"manageCustomers"})

def getCustomersByIdOrName(request):
    '''通过客户id或姓名的方式查询客户信息'''
    keywords = request.GET.get("keywords")
    cur_page = request.GET.get("page")
    global kw
    if keywords is None and kw is None:
        return HttpResponseRedirect("manageCustomers")
    elif keywords is not None:
        kw = keywords

    customer_list = CustomersInfo.objects.filter(Q(id__icontains=kw) |
                                                 Q(cus_name__icontains=kw)).order_by("id").values('id','cus_name','telephone','email','sex','birthday')
    users = zipCustomersData(customer_list)

    cur_user_list, page_num, cur_page, previous_page, next_page = paging(users, cur_page)

    return render(request, 'customers/manage_customers.html', {"users": cur_user_list,
                                                               "page_num": range(1,page_num + 1),
                                                               "cur_page": cur_page,
                                                               "previous_page": previous_page,
                                                               "next_page": next_page,
                                                               "url": "getCustomersByIdOrName"})

def customerFunc(request,cus_func):
    '''根据传入参数调用不同的处理方法'''
    if cus_func == "manageCustomers":
        return getAllCustomers(request)

    elif cus_func == "getCustomersByIdOrName":
        return getCustomersByIdOrName(request)

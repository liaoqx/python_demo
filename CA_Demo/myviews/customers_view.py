# _*_ coding=utf-8 _*_
import logging;logging.basicConfig(level=logging.INFO)
import traceback
from django.http import HttpResponseRedirect
from django.shortcuts import render

def getAllCustomers(request):
    '''获取所有客户信息(cus_name,telephone,email,sex,birthday)'''
    pass


def addCustomer(request):
    ''''''
    pass

def updateCustomerById(request):
    pass

def deleteCustomerById(reqeust):
    pass

def getCustomersByIdOrName(request):
    '''通过客户id或姓名的方式查询客户信息'''
    pass

def getCusCarsById(request):
    '''通过客户id查询该客户拥有的车辆信息,在每行车辆资产信息后添加删除/修改按钮'''
    pass

def customerFunc(request):
    '''根据传入参数调用不同的处理方法'''
    pass
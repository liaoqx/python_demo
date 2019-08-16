# _*_ coding:utf-8 _*_
from django.urls import path
from CA_Demo.myviews import errors_view,customers_view,cars_view
from CA_Demo.myviews import employees_view
from CA_Demo.myviews.clientviews import client_user_views,client_customers_view
import CA_Demo.views
urlpatterns=[
    path('login', CA_Demo.views.login),
    path('exit', CA_Demo.views.exit),
    path('show_<str:html_name>', CA_Demo.views.return_html), #通过参数返回相应的页面
    #path('manage_<str:func>/content_<str:method>', CA_Demo.views.content_manage), #通过参数跳转到func模块下method.html管理页面上
    #path('mytest/manageErrors', CA_Demo.myviews.errors_view.getAllErrors),
    path('errors/<str:err_func>',errors_view.errorsFunc,name="err_view"),

    path('customers/<str:cus_func>',customers_view.customerFunc),

    path('cars/<str:cars_func>',cars_view.carsFunc),

    path('client/user/<str:client_user_func>',client_user_views.clientUserFunc),

    path('client/customer/<str:client_cus_func>',client_customers_view.clientCustomerFunc),

    path('employees/<str:emp_func>',employees_view.employeesFunc)
]
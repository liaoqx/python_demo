# _*_ coding:utf-8 _*_
from django.urls import path
from CA_Demo.myviews import errors_view,customers_view
import CA_Demo.views
urlpatterns=[
    path('login', CA_Demo.views.login),
    path('exit', CA_Demo.views.exit),
    path('show_<str:html_name>', CA_Demo.views.return_html), #通过参数返回相应的页面
    #path('manage_<str:func>/content_<str:method>', CA_Demo.views.content_manage), #通过参数跳转到func模块下method.html管理页面上
    #path('errors/manageErrors', CA_Demo.myviews.errors_view.getAllErrors),
    path('errors/<str:err_func>',errors_view.errorsFunc),

    path('customers/<str:cus_func>',customers_view.customerFunc)
]
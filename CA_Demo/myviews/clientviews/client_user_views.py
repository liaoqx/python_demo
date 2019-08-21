# _*_ coding:utf-8 _*_
'''处理android端客户个人信息请求视图'''
from django.http import HttpResponse
from ...models import CustomersInfo
import logging; logging.basicConfig(level=logging.INFO)
import hashlib
import json

def register(request):
    '''客户注册:id,password,cus_name,telephone,email,sex,birthday'''
    customer = CustomersInfo()
    id = request.POST.get("id")
    logging.info("id = {0}".format(id))
    customer.id = id

    password = request.POST.get("password")

    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    logging.info("pwd_md5:{0}".format(md5.hexdigest()))
    customer.password = md5.hexdigest()

    customer.cus_name = request.POST.get("cus_name")
    telephone = request.POST.get("telephone")
    email = request.POST.get("email")

    if (telephone is None and email is None) or (len(telephone.strip()) == 0 and len(email.strip()) == 0):
        msg = u"联系电话或邮箱必须填写一个!"
        logging.info(msg)
        return HttpResponse(json.dumps({"statusCode":-1,'msg':msg},ensure_ascii=False),content_type='application/json;charset=utf-8')

    if telephone is None:
        customer.telephone = ""
    else:
        customer.telephone = telephone

    if email is None:
        customer.email = ""
    else:
        customer.email = email

    customer.sex = request.POST.get("sex")

    birthday_list = []
    birthday_list.append(id[6:10])
    birthday_list.append(id[10:12])
    birthday_list.append(id[12:14])

    customer.birthday = "-".join(birthday_list)
    logging.info("birthday:{0}".format(customer.birthday))
    customer.save()
    return HttpResponse(json.dumps({"statusCode":0}),content_type='application/json;charset=utf-8')

def login(request):
    pass

def exit(request):
    pass


def updatePwdById(request):
    '''修改客户密码(修改前要验证旧密码,并且新密码与旧密码不能相同)'''
    pass


def updateCusTele(request):
    '''修改客户信息(电话/邮箱地址)'''
    cus_id = request.POST.get("id")
    telephone = request.POST.get("telephone")
    #logging.info("cus_id = {0} , telephone = {1}".format(cus_id,telephone))
    try:
        CustomersInfo.objects.filter(id=cus_id).update(telephone=telephone)
    except CustomersInfo.DoesNotExist:
        msg = u"用户不存在"
        logging.info(msg)
        return HttpResponse(json.dumps({"statusCode":-1,"msg":msg},ensure_ascii=False),content_type='application/json;charset=utf-8')
    else:
        return HttpResponse(json.dumps({"statusCode":0}),content_type='application/json;charset=utf-8')


def updateCusEmail(request):
    cus_id = request.POST.get("id")
    email = request.POST.get("email")
    try:
        CustomersInfo.objects.filter(id=cus_id).update(email=email)
    except CustomersInfo.DoesNotExist:
        msg = u"用户不存在"
        logging.info(msg)
        return HttpResponse(json.dumps({"statusCode":-1,"msg":msg},ensure_ascii=False),content_type='application/json;charset=utf-8')
    else:
        return HttpResponse(json.dumps({"statusCode":0}),content_type='application/json;charset=utf-8')

def getCustomerById(request):
    '''根据客户id获取用户个人信息'''
    cus_id = request.POST.get("id")
    customer = CustomersInfo.objects.filter(id = cus_id).values('cus_name','telephone','email','sex','birthday').first()
    customer['birthday'] = customer['birthday'].strftime("%Y-%m-%d")

    #logging.info("cusInfo:{0}".format(customer)) #cusInfo:{'cus_name': '项羽', 'telephone': '19900010002', 'email': '123456@exmaple.com', 'sex': 'M', 'birthday': '1987-08-07'}

    return HttpResponse(json.dumps(str(customer),ensure_ascii=False),content_type='application/json;charset=utf-8')


def deleteCustomerById(request):
    '''注销用户'''
    cus_id = request.POST.get("id")
    CustomersInfo.objects.filter(id=cus_id).delete()
    return HttpResponse(json.dumps({"statusCode":0}),content_type="application/json;charset=utf-8")


def clientUserFunc(request,client_user_func):
    if client_user_func == "register":
        return register(request)

    elif client_user_func == "updateCusTele":
        return updateCusTele(request)

    elif client_user_func == 'updateCusEmail':
        return updateCusEmail(request)

    elif client_user_func == "deleteCustomerById":
        return deleteCustomerById(request)

    elif client_user_func == "getCustomerById":
        return getCustomerById(request)
# _*_ coding:utf-8 _*_
'''处理用户-车辆信息请求视图'''
import logging; logging.basicConfig(level=logging.INFO)
from django.http import HttpResponse
from ...models import CarsInfo,UserCarsInfo
import json

color_list = [6,u'黑色',u'白色',u'灰色',u'蓝色',u'红色',u'紫色']  #车型色系

def getCusCarsById(request):
    '''通过客户id查询该客户拥有的车辆信息'''
    cus_id = request.POST.get("id")
    car_list = UserCarsInfo.objects.filter(customer_id = cus_id).values('plate_number','car_id','color')

    for car in car_list:    #将颜色编号转换为对应的颜色名称
        car['color'] = color_list[int(car['color'])]

    #logging.info("car_list:{0}".format(car_list))
    #<QuerySet [{'plate_number': '渝AXY001', 'car_id': 'CA2016-08-MB', 'color': '黑色'},
    #           {'plate_number': '渝AXY002', 'car_id': 'CA2016-08-JC', 'color': '黑色'}]>
    return HttpResponse(json.dumps(str(car_list),ensure_ascii=False),content_type='application/json;charset=utf-8')


def getAllCars(request):
    car_list = CarsInfo.objects.all().values()

    for car in car_list:
        car['produce_time'] = car['produce_time'].strftime("%Y-%m-%d")

    #logging.info("cars:{0}".format(car_list))
    #cars: < QuerySet[{'car_id': 'BC2008-05-JC', 'car_name': '奥运专用轿车', 'produce_time': '2008-05-20', 'car_weight': 2000,'allowable_weight': 1000,
    #                               'power': 3500, 'engine': 'FDJ002', 'number': 5, 'color_list': '456','is_removed': 'T', 'remark': ''},
    #                 {'car_id': 'CA2018-06-JC', 'car_name': '小轿车002', 'produce_time': '2018-06-26', 'car_weight': 2500,'allowable_weight': 800,
    #                   'power': 2000, 'engine': 'FDJ002', 'number': 4, 'color_list': '123456','is_removed': 'T', 'remark': '销量较好'}]>

    return HttpResponse(json.dumps(str(car_list),ensure_ascii=False),content_type="application/json;charset=utf-8")

def addCusCars(request):
    '''客户添加车辆资产'''
    '''先获取所有车辆类型'''
    cus_id = request.POST.get("id")
    cars_list = request.POST.get("cars") #获取添加的所有车辆

    for carinfo in cars_list:
        car = UserCarsInfo()
        car.customer_id = carinfo.customer_id
        car.plate_number = carinfo.plate_number
        car.color = carinfo.color
        car.save()
    return HttpResponse(json.dumps({"statusCode":0}),content_type='application/json;charset=utf-8')

def updateCusCarById(request):
    '''通过客户id和car_id修改客户与车辆的绑定关系'''
    '''根据发送的车牌号决定对用户-车辆信息进行添加或删除'''
    pass


def clientCustomerFunc(request,client_cus_func):
    if client_cus_func == "getAllCars":
        return getAllCars(request)

    elif client_cus_func == "addCusCars":
        return addCusCars(request)

    elif client_cus_func == "getCusCarsById":
        return getCusCarsById(request)
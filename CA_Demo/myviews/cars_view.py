#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from ..models import CarsInfo,CarComponentsInfo,UserCarsInfo
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import Q
import logging;logging.basicConfig(level=logging.INFO)
from .tools import paging

color_list = [6,u'黑色',u'白色',u'灰色',u'蓝色',u'红色',u'紫色']  #车型色系
kw = None

def zipCarsData(car_list):
    cars = []
    for c in car_list:
        car = {}
        colors = []
        color_list_number = map(int,list(c.color_list)) #将车型色系代号转换为数字 c.color_list 的格式为：'123456'
        #logging.info("color_list_int:{0}".format(list(color_list_number))
        for color_pos in list(color_list_number):  # 获取该种车型的色系的每个颜色代号
            colors.append(color_list[color_pos])  # 将颜色代号转换为对应颜色

        #格式化日期
        # %y 两位数的年份表示（00-99）   %Y 四位数的年份表示（0000-9999）  %m 月份（01-12）  %d 月内中的一天（0-31）
        # %H 24小时制小时数（0-23）  %I 12小时制小时数（01-12）  %M 分钟数（00=59）  %S 秒（00-59）
        c.produce_time = c.produce_time.strftime("%Y-%m-%d") #strftime("%Y-%m-%d %H:%I:%S")
        car['car'] = c
        car['color_list'] = colors
        cars.append(car)
    return cars

def getAllCars(request):
    '''获取所有车辆信息'''
    cur_page = request.GET.get("page")
    car_list = CarsInfo.objects.all().order_by("car_id")
    cars = zipCarsData(car_list)
    #logging.info("cars:{0}".format(cars))
    cur_car_list,page_num,cur_page,previous_page,next_page = paging(cars,cur_page)
    return render(request,'cars/manage_cars.html',{"car_list":cur_car_list,
                                                   "page_num":range(1,page_num + 1),
                                                   "cur_page":cur_page,
                                                   "previous_page":previous_page,
                                                   "next_page":next_page,
                                                   "url":"manageCars"})

def getCarsByIdOrName(request):
    '''通过车辆型号/名称查询车辆信息'''
    keywords = request.GET.get("keywords")
    cur_page = request.GET.get("page")

    global kw
    if keywords is None and kw is None:
        return HttpResponseRedirect("manageCars")

    elif keywords is not None:
        kw = keywords

    car_list = CarsInfo.objects.filter(Q(car_id__icontains=kw) | Q(car_name__icontains=kw)).order_by("car_id")
    cars = zipCarsData(car_list)
    #logging.info("cars:{0}".format(cars))
    cur_car_list,page_num,cur_page,previous_page,next_page = paging(cars,cur_page)
    return render(request,'cars/manage_cars.html',{"car_list":cur_car_list,
                                                   "page_num":range(1,page_num + 1),
                                                   "cur_page":cur_page,
                                                   "previous_page":previous_page,
                                                   "next_page":next_page,
                                                   "url":"getAllCars"})

def getEngines():
    '''获取发动机信息'''
    engines = CarComponentsInfo.objects.filter(component_id__startswith='FDJ',is_removed = 'F')
    #logging.info("engines:{0}".format(engines))
    return engines


def getRequestCarData(request):
    car = CarsInfo()
    car.car_id = request.POST.get("car_id")
    car.car_name = request.POST.get("car_name")
    car.produce_time = request.POST.get("produce_time")
    car.car_weight = request.POST.get("car_weight")
    car.allowable_weight = request.POST.get("allowable_weight")
    car.power = request.POST.get("power")
    car.engine = request.POST.get("engine")
    car.number = request.POST.get("number")
    car.color_list = request.POST.get("colors")

    #logging.info("color_list:{0}".format(car.color_list))

    car.is_removed = request.POST.get("is_removed")
    car.remark = request.POST.get("remark")
    return car

def addCar(request):
    '''添加车辆'''
    car = getRequestCarData(request)
    car.save()
    return HttpResponseRedirect('manageCars')

def updateCarById(request):
    '''根据车辆型号修改车辆信息'''
    oldCarId = request.POST.get("oldCarId")
    car = getRequestCarData(request)
    CarsInfo.objects.filter(car_id = oldCarId).update(car_id = car.car_id,car_name = car.car_name,
                                                      produce_time = car.produce_time,car_weight = car.car_weight,allowable_weight = car.allowable_weight,
                                                      power = car.power,engine = car.engine,number = car.number,
                                                      color_list = car.color_list,is_removed = car.is_removed,remark = car.remark)
    return HttpResponseRedirect('manageCars')


def deleteCarById(request):
    '''根据车辆型号删除车辆信息'''
    ids = request.GET.get("ids")
    ids_list = []
    for id in ids.split(","):
        ids_list.append(id)
    #logging.info("ids_list:{0}".format(ids_list))
    user_cars = UserCarsInfo.objects.filter(car_id__in=ids_list).values('car_id').distinct()  #获取待删车辆中仍和用户有关联的车辆型号
    logging.info("user_cars:{0}".format(user_cars))

    user_cars_list = []  #存储待删车辆中仍和用户有关联的车辆型号
    for car in user_cars:
        user_cars_list.append(car['car_id'])
        ids_list.remove(car['car_id'])  #留下与用户没有关联关系的车辆型号

    CarsInfo.objects.filter(car_id__in = user_cars_list).update(is_removed = 'T')
    CarsInfo.objects.filter(car_id__in = ids_list).delete()

    return HttpResponseRedirect('manageCars')

def carsFunc(request,cars_func):
    '''根据参数调用不同的车辆模块函数'''
    if cars_func == "manageCars":
        return getAllCars(request)

    elif cars_func == "getCarsByIdOrName":
        return getCarsByIdOrName(request)

    elif cars_func == "toUpdateCarById":
        car_id = request.GET.get("car_id")
        car = CarsInfo.objects.get(car_id = car_id)
        carInfo = {}
        car.produce_time = car.produce_time.strftime("%Y-%m-%d")
        carInfo['car'] = car
        carInfo['color_list'] = list(map(int,list(car.color_list)))
        carInfo['engines'] = getEngines()
        return render(request,'cars/updateCar.html',{"carInfo":carInfo})

    elif cars_func == "toAddCar":

        return render(request,'cars/addCar.html',{"engines":getEngines()})

    elif cars_func == "addCar":
        return addCar(request)

    elif cars_func == "updateCarById":
        return updateCarById(request)

    elif cars_func == "deleteCarById":
        return deleteCarById(request)
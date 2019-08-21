# _*_ coding:utf-8 _*_
from django.shortcuts import render
from ..models import CarComponentsInfo,CarsInfo
import logging;

logging.basicConfig(level=logging.INFO)
from django.http import HttpResponseRedirect
from django.db.models import Q
import traceback
from .tools import paging


# Create your myviews here.
def getAllComponents(request):
    '''获取所有部件信息'''
    cur_page = request.GET.get("page")
    component_list = CarComponentsInfo.objects.all().order_by("component_id")
    #logging.info("getAllErrors: {err}".format(err=error_list))
    cur_com_list, page_num, cur_page, previous_page, next_page = paging(component_list, cur_page)
    return render(request, 'carcomponents/manage_Components.html', {'component_list': cur_com_list,
                                                                    'page_num': range(1, page_num + 1),
                                                                    'cur_page': cur_page,
                                                                    'previous_page': previous_page,
                                                                    'next_page': next_page,
                                                                    'url': 'manageComponents'
                                                                    })


def addComponent(request):
    '''添加部件信息'''
    component_id=request.POST.get('component_id')
    component_name=request.POST.get('component_name')
    manufacture=request.POST.get('manufacture')
    price=request.POST.get('price')
    func_param=request.POST.get('func_param')
    is_removed=request.POST.get('is_removed')
    remark=request.POST.get('remark')
    if component_id.strip() == "" or component_name.strip() == "" or manufacture.strip() == "" or price.strip()=="" or func_param.strip()=="" or is_removed.strip()=="" or remark.strip() == "":
        warning = u"请完善信息后再提交!"
        return render(request, 'carcomponents/addComponents.html', {'status': -1,
                                                        'component_id': component_id,
                                                        'component_name': component_name,
                                                        'manufacture': manufacture,
                                                        'price': price,
                                                        'func_param': func_param,
                                                        'is_removed': is_removed,
                                                        'remark': remark,
                                                        'warning': warning})
    component = CarComponentsInfo(component_id=component_id, component_name=component_name, manufacture=manufacture, price=price, func_param=func_param, is_removed=is_removed,remark=remark)
    try:
        component.save()
    except BaseException:
        traceback.print_exc()
        warning = u"操作失败"
        return render(request, 'carcomponents/addComponents.html', {'status': -1,
                                                         'component_id': component_id,
                                                        'component_name': component_name,
                                                        'manufacture': manufacture,
                                                        'price': price,
                                                        'func_param': func_param,
                                                        'is_removed': is_removed,
                                                        'remark': remark,
                                                        'warning': warning})
    else:
        return HttpResponseRedirect('manageComponents')


def updateComponentById(request):
    '''修改部件信息'''
    oldId = request.GET.get("oldId")
    component_id = request.POST.get('component_id')
    component_name = request.POST.get('component_name')
    manufacture = request.POST.get('manufacture')
    price = request.POST.get('price')
    func_param = request.POST.get('func_param')
    is_removed = request.POST.get('is_removed')
    remark = request.POST.get("remark")
    #logging.info("oldId <{0}>,newId <{1}>".format(oldId, err_code))
    try:
        CarComponentsInfo.objects.filter(component_id=oldId).update(component_id=component_id, component_name=component_name, manufacture=manufacture, price=price, func_param=func_param, is_removed=is_removed,remark=remark)

    except BaseException:
        traceback.print_exc()
        return HttpResponseRedirect('toUpdateComponentById?component_id={0}'.format(oldId))
    else:
        return HttpResponseRedirect('manageComponents')


def deleteComponentById(request):
    '''删除部件信息'''
    ids = request.GET.get("component_id")
    ids_list = []
    for id in ids.split(","): #构造由待删除记录id编号组成的数组
        ids_list.append(id)
    #logging.info("deleteErrors' ids:<{0}>; ids_list:<{1}>".format(ids,ids_list))
    engines = CarsInfo.objects.filter(engine__in=ids_list).values("engine").distinct()
    logging.info("engines:{0}".format(engines))
    using_id_list = []
    for engine in engines:
        using_id_list.append(engine['engine'])
        ids_list.remove(engine['engine'])

    CarComponentsInfo.objects.filter(component_id__in=using_id_list).update(is_removed='T')
    CarComponentsInfo.objects.filter(component_id__in=ids_list).delete()  #批量删除数据
    return HttpResponseRedirect('manageComponents')


def getComponentsByIdOrName(request):
    '''通过部件编号/名称查询部件信息'''
    keywords = request.GET.get("keywords")
    #logging.info("keywords: <{0}>".format(keywords))
    if keywords is None:
        return HttpResponseRedirect('manageComponents')

    component_list = CarComponentsInfo.objects.filter(
        Q(component_id__icontains=keywords) | Q(component_name__icontains=keywords)
    ).order_by("component_id")
    #logging.info("getErrorsByIdOrName :{0}".format(err_list))
    return render(request, 'carcomponents/manage_Components.html', {'component_list': component_list})


def componentFunc(request, com_func):
    # logging.info(com_func)
    if com_func == 'manageComponents':
        return getAllComponents(request)

    elif com_func == 'toAddComponent':
        return render(request, 'carcomponents/addComponents.html')

    elif com_func == "addComponents":
        return addComponent(request)

    elif com_func == "getComponentsByIdOrName":
        return getComponentsByIdOrName(request)

    elif com_func == "toUpdateComponentById":
        component_id = request.GET.get("component_id")
        component = CarComponentsInfo.objects.get(component_id=component_id)
        return render(request, 'carcomponents/updateComponent.html', {'component': component})

    elif com_func == "updateComponentById":
        return updateComponentById(request)

    elif com_func == "deleteComponentById":
        return deleteComponentById(request)

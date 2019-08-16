#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.shortcuts import render,redirect
from ..models import ErrorsInfo
import logging;

logging.basicConfig(level=logging.INFO)
from django.http import HttpResponseRedirect
from django.db.models import Q
import traceback

from .tools import paging

kw = None

# Create your myviews here.
def getAllErrors(request):
    '''获取所有故障信息'''
    cur_page = request.GET.get("page")

    error_list = ErrorsInfo.objects.all().order_by("err_code")
    cur_error_list,page_num,cur_page,previous_page,next_page = paging(error_list,cur_page)

    #logging.info("getAllErrors: {err}".format(err=error_list))
    return render(request, 'errors/manage_errors.html', {'error_list': cur_error_list,
                                                         'page_num':range(1,page_num+1),
                                                         'cur_page':cur_page,
                                                         'previous_page':previous_page,
                                                         'next_page':next_page,
                                                         'url':'manageErrors'})


def addError(request):
    '''添加故障信息'''
    err_code = request.POST.get('err_code')
    err_desc = request.POST.get('err_desc')
    remark = request.POST.get('remark')
    warning = ""
    if err_code.strip() == "" or \
            err_desc.strip() == "" or remark.strip() == "":
        warning = u"请完善信息后再提交!"
        return render(request, 'errors/addError.html', {'status': -1,
                                                        'err_code': err_code,
                                                        'err_desc': err_desc,
                                                        'remark': remark,
                                                        'warning': warning})
    err = ErrorsInfo(err_code=err_code, err_desc=err_desc, remark=remark)
    try:
        err.save()
    except BaseException:
        traceback.print_exc()
        warning = u"操作失败"
        return render(request, 'errors/addError.html', {'status': -1,
                                                        'err_code': err_code,
                                                        'err_desc': err_desc,
                                                        'remark': remark,
                                                        'warning': warning})
    else:
        warning = u"操作成功"
        # request.session['status'] = 0
        # request.session['warning'] = warning
        #return HttpResponseRedirect('manageErrors')
        return redirect("err_view",err_func = "manageErrors")


def updateErrorById(request):
    '''修改故障信息'''
    oldId = request.POST.get("oldId")
    err_code = request.POST.get("err_code")
    err_desc = request.POST.get("err_desc")
    remark = request.POST.get("remark")
    #logging.info("oldId <{0}>,newId <{1}>".format(oldId, err_code))
    try:
        ErrorsInfo.objects.filter(err_code=oldId).update(err_code=err_code, err_desc=err_desc, remark=remark)

    except BaseException:
        traceback.print_exc()
        return HttpResponseRedirect('toUpdateErrorById?err_code={0}'.format(oldId))
    else:
        return HttpResponseRedirect('manageErrors')


def deleteErrorById(request):
    '''删除故障信息'''
    ids = request.GET.get("err_code")
    ids_list = []
    for id in ids.split(","): #构造由待删除记录id编号组成的数组
        ids_list.append(id)
    #logging.info("deleteErrors' ids:<{0}>; ids_list:<{1}>".format(ids,ids_list))
    ErrorsInfo.objects.filter(err_code__in=ids_list).delete()  #批量删除数据
    return HttpResponseRedirect('manageErrors')


def getErrorsByIdOrName(request):
    '''通过故障编号/名称查询故障信息'''
    keywords = request.GET.get("keywords")
    cur_page = request.GET.get("page")

    global kw
    if keywords is None and kw is None: #之前没有用关键字搜索过,且此次搜索关键字为空 -> 默认返回所有记录
        return HttpResponseRedirect('manageErrors')

    elif keywords is not None: #每次有新的请求 -> 更换关键字
        kw = keywords

    err_list = ErrorsInfo.objects.filter(Q(err_code__icontains=kw)
                                         | Q(err_desc__icontains=kw)).order_by("err_code")

    cur_error_list,page_num,cur_page,previous_page,next_page = paging(err_list,cur_page)

    #logging.info("getErrorsByIdOrName -- err_list :{0}".format(err_list_bySearch))
    #logging.info("getErrorsByIdOrName -- cur_error_list:{0}".format(cur_error_list))
    return render(request, 'errors/manage_errors.html', {'error_list': cur_error_list,
                                                         'page_num': range(1, page_num + 1),
                                                         'cur_page': cur_page,
                                                         'previous_page': previous_page,
                                                         'next_page': next_page,
                                                         'url':'getErrorsByIdOrName'})


def errorsFunc(request, err_func):
    # logging.info(err_func)
    if err_func == 'manageErrors':
        return getAllErrors(request)

    elif err_func == 'toAddError':
        return render(request, 'errors/addError.html')

    elif err_func == "addError":
        return addError(request)

    elif err_func == "getErrorsByIdOrName":
        return getErrorsByIdOrName(request)

    elif err_func == "toUpdateErrorById":
        err_code = request.GET.get("err_code")
        error = ErrorsInfo.objects.get(err_code=err_code)
        return render(request, 'errors/updateError.html', {'error': error})

    elif err_func == "updateErrorById":
        return updateErrorById(request)

    elif err_func == "deleteErrorById":
        return deleteErrorById(request);

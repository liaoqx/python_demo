# _*_ coding:utf-8 _*_
from django.shortcuts import render
from ..models import ErrorsInfo
import logging;

logging.basicConfig(level=logging.INFO)
from django.http import HttpResponseRedirect
from django.db.models import Q
import traceback


# Create your myviews here.
def getAllErrors(request):
    '''获取所有故障信息'''
    error_list = ErrorsInfo.objects.all()
    #logging.info("getAllErrors: {err}".format(err=error_list))
    return render(request, 'errors/manage_errors.html', {'error_list': error_list})


def addError(request):
    '''添加故障信息'''
    err_code = request.POST.get('err_code')
    err_desc = request.POST.get('err_desc')
    remark = request.POST.get('remark')
    warning = ""
    if err_code.strip() == "" or \
            err_desc.strip() == "" or remark.strip() == "":
        warning = "请完善信息后再提交!"
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
        warning = "操作失败"
        return render(request, 'errors/addError.html', {'status': -1,
                                                        'err_code': err_code,
                                                        'err_desc': err_desc,
                                                        'remark': remark,
                                                        'warning': warning})
    else:
        warning = "操作成功"
        # request.session['status'] = 0
        # request.session['warning'] = warning
        return HttpResponseRedirect('manageErrors')


def updateErrorById(request):
    '''修改故障信息'''
    oldId = request.GET.get("oldId")
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
    #logging.info("keywords: <{0}>".format(keywords))
    if keywords is None:
        return HttpResponseRedirect('manageErrors')

    err_list = ErrorsInfo.objects.filter(
        Q(err_code__icontains=keywords) | Q(err_desc__icontains=keywords)
    )
    #logging.info("getErrorsByIdOrName :{0}".format(err_list))
    return render(request, 'errors/manage_errors.html', {'error_list': err_list})


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

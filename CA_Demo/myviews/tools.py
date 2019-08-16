#!/usr/bin/env python
# _*_ coding:utf-8 _*_
#各模块公用的数据处理函数
from django.core.paginator import Paginator
def paging(data_list,cur_page):
    '''分页处理:总数据源,当前页页码'''
    num = 3  #每页显示的记录数量
    if cur_page:
        cur_page = int(cur_page)
    else:
        cur_page = 1  #若未传入当前页页码,则默认为首页
    paginator = Paginator(data_list, num)  # 设置每页显示三行信息
    page_num = paginator.num_pages  # 获取总页数

    cur_data_list = paginator.page(cur_page)  # 获取当前页内容

    # 计算当前页的上一页页码
    if cur_data_list.has_previous():  # 当前页是否有上一页;
        previous_page = cur_page - 1
    else:
        previous_page = cur_page

    # 计算当前页的下一页页码
    if cur_data_list.has_next():
        next_page = cur_page + 1
    else:
        next_page = cur_page
    return cur_data_list,page_num,cur_page,previous_page,next_page
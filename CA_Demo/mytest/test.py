# _*_ coding:utf-8 _*_
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_demo.settings')
django.setup()
from CA_Demo.models import EmployeesInfo
import hashlib
import logging;

logging.basicConfig(level=logging.INFO)
from datetime import date


def addEmployee():
    emp = EmployeesInfo()
    pwd = '123456'
    emp.id = '500001198706180001'
    emp.emp_id = 'ED01A001'
    emp.emp_name = '胡汉三'

    md5 = hashlib.md5()
    md5.update(pwd.encode('utf-8'))
    emp.password = md5.hexdigest()

    logging.info("<pwd:{pwd}>".format(pwd=emp.password))

    emp.email = '123456789@example.com'
    emp.is_admin = 'T'
    emp.emp_dept = 'ED01'
    emp.sex = 'M'
    emp.join_time = date(2016, 10, 1)
    emp.telephone = '199000000001'
    emp.save()

def getEmployee():
    emp = EmployeesInfo.objects.all()[0]
    logging.info("<emp.name : {name}>".format(name=emp.emp_name))
    try:
        emp2 = EmployeesInfo.objects.get(id='001')
    except EmployeesInfo.DoesNotExist:
        emp2 = None
    if emp2:
        logging.info("<emp2.name : {name}>".format(name=emp2.emp_name))
    else:
        logging.info("Not exists...")



if __name__ == '__main__':
    addEmployee()
    getEmployee()

#_*_ coding:utf-8 _*_
from django.test import TestCase
from .models import EmployeesInfo
import hashlib
import logging;logging.basicConfig(level = logging.INFO)
from datetime import date

# Create your tests here.
class EmployeeTest(TestCase):
    def test_addEmployee(self):
        emp = EmployeesInfo()
        pwd = '123456'
        emp.id = '500001198706180001'
        emp.emp_id = 'ED01A001'
        emp.emp_name = '胡汉三'.encode('utf-8')
        md5 = hashlib.md5()
        md5.update(pwd.encode('utf-8'))
        print(md5.hexdigest())

        emp.password = md5.hexdigest()

        logging.info("<pwd:{pwd}>".format(pwd=emp.password))
        emp.email = '123456789@example.com'
        emp.is_admin = 'T'
        emp.emp_dept = 'ED01'
        emp.sex = 'M'
        emp.join_time = date(2016, 10, 1)
        emp.telephone = '199000000001'
        emp.save()



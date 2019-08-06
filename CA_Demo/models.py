# _*_ coding:utf-8 _*_
from django.db import models

# 故障信息列
class ErrorsInfo(models.Model):
    err_code = models.CharField(max_length=32,unique=True,null=False) #错误代码
    err_desc = models.CharField(max_length=256)                       #错误描述
    remark = models.CharField(max_length=128)                         #备注(修复建议)
    def __str__(self):
        return self.err_code
    class Meta:
        db_table = 'errors_info'


#客户信息
class CustomersInfo(models.Model):
    id = models.CharField(max_length=18,primary_key=True)   #身份证号
    cus_name = models.CharField(max_length=32,null=False)   #姓名
    password = models.CharField(max_length=16,null=False)   #密码 6-16位
    telephone = models.CharField(max_length=16)             #联系方式
    email = models.CharField(max_length=32)                 #邮件(联系方式,必须填写一个)
    sex = models.CharField(max_length=1)                    #性别 F:女 M:男
    birthday = models.DateField()                           #出生日期
    def __str__(self):
        return self.cus_name
    class Meta:
        db_table = 'customers_info'


#员工信息
class EmployeesInfo(models.Model):
    id = models.CharField(max_length=18,primary_key=True)           #身份证号
    emp_id = models.CharField(max_length=18,unique=True,null=False) #员工编号
    emp_name = models.CharField(max_length=64,null=False)           #员工姓名
    password = models.CharField(max_length=16)                      #密码,若为管理员则不能为空
    is_admin = models.CharField(max_length=1,default='F')           #是否为管理员用户,T:是 F:否
    telephone = models.CharField(max_length=16)                     #联系方式
    email = models.CharField(max_length=32)                         #邮件(联系方式,必须填写一个)
    sex = models.CharField(max_length=1)                            #性别 F:女 M:男
    join_time = models.DateField()                                  #入职时间
    # 所在部门 ED001:人力资源部 ED002:财务部    3:运维部 4:研发部 5:质量监察部 6:营销部
    emp_dept = models.CharField(max_length=4)
    is_removed = models.CharField(max_length=1,default='F')  # 是否被逻辑删除 T:是  F:否
    def __str__(self):
        return self.emp_name
    class Meta:
        db_table = 'employees_info'


#车辆信息
class CarsInfo(models.Model):
    car_id = models.CharField(max_length=32,unique=True,null=False)     #车辆型号
    car_name = models.CharField(max_length=64)                          #车辆名称
    produce_time = models.DateField()                                   #出厂时间
    car_weight = models.IntegerField()                                  #总质量(kg)
    allowable_weight = models.IntegerField()                            #额定承重量(kg)
    power = models.IntegerField()                                       #电机功率(kw)
    engine = models.CharField(max_length=32)                            #发动机型号
    number = models.IntegerField()                                      #乘员数
    # 车身颜色 1:黑色 2:白色 3:灰色 4:蓝色 5:红色 6:紫色
    color_list = models.CharField(max_length=8)
    is_removed = models.CharField(max_length=1,default='F')             # 是否被逻辑删除 T:是  F:否
    remark = models.CharField(max_length=128)                           #备注
    def __str__(self):
        return self.car_id.join(self.car_name)
    class Meta:
        db_table = 'cars_info'


#车辆部件信息
class CarComponentsInfo(models.Model):
    component_id = models.CharField(max_length=16,unique=True,null=False)   #部件编号
    component_name = models.CharField(max_length=32)                        #部件名称
    manufacture = models.CharField(max_length=64)                           #生产厂商
    price = models.DecimalField(max_digits=9,decimal_places=2)              #单价 保存2位小数,共9位数
    func_param = models.CharField(max_length=64)                            #性能参数
    is_removed = models.CharField(max_length=1,default='F')                 #是否被逻辑删除 T:是  F:否
    remark = models.CharField(max_length=128)                               #备注
    def __str__(self):
        return self.component_id.join(self.component_name)
    class Meta:
        db_table = 'car_components_info'

#用户-车辆信息
class UserCarsInfo(models.Model):
    cus_id = models.ForeignKey(CustomersInfo,on_delete=models.CASCADE,verbose_name='car_owner_id')  #车主编号
    car_id = models.ForeignKey(CarsInfo,on_delete=models.PROTECT,verbose_name='car_id')  #车辆编号
    color = models.CharField(max_length=1) #车身颜色
    def __str__(self):
        return self.cus_id.join(self.car_id)
    class Meta:
        db_table = 'user_cars_info'

#维修记录
class RepairInfo(models.Model):
    cus_id = models.ForeignKey(CustomersInfo,on_delete=models.CASCADE,verbose_name='repair_cus_id') #维修客户的编号
    car_id = models.ForeignKey(CarsInfo,on_delete=models.PROTECT,verbose_name='repair_car_id')       #维修车辆的编号
    emp_id = models.ForeignKey(EmployeesInfo,on_delete=models.PROTECT,verbose_name='repair_emp_id')  #维修人员的编号
    repair_desc = models.CharField(max_length=128)                          #故障描述
    repair_time = models.DateTimeField(auto_now=True,null=False)            #维修时间
    def __str__(self):
        return self.cus_id.join(self.car_id).join(self.repair_time)
    class Meta:
        db_table = 'repair_info'
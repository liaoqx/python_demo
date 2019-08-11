# _*_ coding:utf-8 _*_
from django.db import models

# 故障信息
class ErrorsInfo(models.Model):
    err_code = models.CharField(primary_key=True,max_length=32,verbose_name="故障代码") #错误代码
    err_desc = models.CharField(max_length=256,verbose_name="故障描述")                       #错误描述
    remark = models.CharField(max_length=128,verbose_name="修复建议")                         #备注(修复建议)
    def __str__(self):
        return self.err_code
    class Meta:
        db_table = 'errors_info'
        verbose_name = '故障信息'
        verbose_name_plural = verbose_name


#客户信息
class CustomersInfo(models.Model):
    id = models.CharField(max_length=18,primary_key=True,verbose_name="身份证号")   #身份证号
    cus_name = models.CharField(max_length=32,null=False,verbose_name="姓名")        #姓名
    password = models.CharField(max_length=32,null=False,verbose_name="密码")     #密码 6-16位
    telephone = models.CharField(max_length=16,verbose_name="联系方式")             #联系方式
    email = models.CharField(max_length=32,verbose_name="邮件")                 #邮件(联系方式,必须填写一个)
    sex = models.CharField(max_length=1,verbose_name="性别")                    #性别 F:女 M:男
    birthday = models.DateField(verbose_name="出生日期")                           #出生日期
    def __str__(self):
        return self.cus_name
    class Meta:
        db_table = 'customers_info'
        verbose_name = "客户信息"
        verbose_name_plural = verbose_name


#员工信息
class EmployeesInfo(models.Model):
    id = models.CharField(max_length=18,primary_key=True,verbose_name="身份证号")           #身份证号
    emp_id = models.CharField(max_length=18,unique=True,null=False,verbose_name="员工编号") #员工编号
    emp_name = models.CharField(max_length=64,null=False,verbose_name="员工姓名")          #员工姓名
    password = models.CharField(max_length=32,verbose_name="密码")                         #密码,若为管理员则不能为空
    is_admin = models.CharField(max_length=1,default='F',verbose_name="是否为管理员")       #是否为管理员用户,T:是 F:否
    telephone = models.CharField(max_length=16,verbose_name="联系方式")                    #联系方式
    email = models.CharField(max_length=32,verbose_name="邮件")                            #邮件(联系方式,必须填写一个)
    sex = models.CharField(max_length=1,verbose_name="性别")                               #性别 F:女 M:男
    join_time = models.DateField(verbose_name="入职时间")                                  #入职时间
    # 所在部门 ED001:人力资源部 ED002:财务部    3:运维部 4:研发部 5:质量监察部 6:营销部
    emp_dept = models.CharField(max_length=4,verbose_name="所在部门")
    is_removed = models.CharField(max_length=1,default='F',verbose_name="是否在职")  # 是否被逻辑删除 T:是  F:否
    def __str__(self):
        return self.emp_id + self.emp_name
    class Meta:
        db_table = 'employees_info'
        verbose_name = "员工信息"
        verbose_name_plural = verbose_name


#车辆信息
class CarsInfo(models.Model):
    car_id = models.CharField(primary_key=True,max_length=32,verbose_name="车辆型号")     #车辆型号
    car_name = models.CharField(max_length=64,verbose_name="车辆名称")                          #车辆名称
    produce_time = models.DateField(verbose_name="出厂时间")                                   #出厂时间
    car_weight = models.IntegerField(verbose_name="总质量(kg)")                                  #总质量(kg)
    allowable_weight = models.IntegerField(verbose_name="额定承重量(kg)")                            #额定承重量(kg)
    power = models.IntegerField(verbose_name="电机功率(kw)")                                       #电机功率(kw)
    engine = models.CharField(max_length=32,verbose_name="发动机型号")                            #发动机型号
    number = models.IntegerField(verbose_name="乘员数")                                      #乘员数
    # 车身颜色 1:黑色 2:白色 3:灰色 4:蓝色 5:红色 6:紫色
    color_list = models.CharField(max_length=8,verbose_name="色系")
    is_removed = models.CharField(max_length=1,default='F',verbose_name="生产状态")             # 是否被逻辑删除 T:是(停产)  F:否(在产)
    remark = models.CharField(max_length=128,verbose_name="备注")                           #备注
    def __str__(self):
        return self.car_id + self.car_name
    class Meta:
        db_table = 'cars_info'
        verbose_name = "车辆信息"
        verbose_name_plural = verbose_name


#车辆部件信息
class CarComponentsInfo(models.Model):
    component_id = models.CharField(primary_key=True,max_length=16,verbose_name="部件编号")   #部件编号
    component_name = models.CharField(max_length=32,verbose_name="部件名称")                        #部件名称
    manufacture = models.CharField(max_length=64,verbose_name="生产厂商")                           #生产厂商
    price = models.FloatField(verbose_name="单价")              #max_digits=9,decimal_places=2,单价 保存2位小数,共9位数
    func_param = models.CharField(max_length=64,verbose_name="性能参数")                            #性能参数
    is_removed = models.CharField(max_length=1,default='F',verbose_name="是否还在生产")                 #是否被逻辑删除 T:是  F:否
    remark = models.CharField(max_length=128,verbose_name="备注")                               #备注
    def __str__(self):
        return self.component_id + self.component_name
    class Meta:
        db_table = 'car_components_info'
        verbose_name = "车辆部件信息"
        verbose_name_plural = verbose_name

#用户-车辆信息
class UserCarsInfo(models.Model):
    plate_number = models.CharField(primary_key=True,max_length=8,verbose_name="车牌号") #车牌号
    customer = models.ForeignKey(CustomersInfo,on_delete=models.CASCADE,verbose_name='车主姓名')  #车主
    car = models.ForeignKey(CarsInfo,on_delete=models.PROTECT,verbose_name='车辆型号')  #车辆型号
    color = models.CharField(max_length=1,verbose_name="车身颜色") #车身颜色
    def __str__(self):
        return self.customer.cus_name + " " + self.car.car_id
    class Meta:
        db_table = 'user_cars_info'
        verbose_name = "用户-车辆信息"
        verbose_name_plural = verbose_name

#维修记录
class RepairInfo(models.Model):
    customer = models.ForeignKey(CustomersInfo,on_delete=models.CASCADE,verbose_name='客户姓名') #维修客户
    employee = models.ForeignKey(EmployeesInfo,on_delete=models.PROTECT,verbose_name='维修人员')  #维修人员
    plate_number = models.CharField(max_length=8,verbose_name="车牌号")    #车牌号
    repair_desc = models.CharField(max_length=128,verbose_name="故障描述")                          #故障描述
    repair_time = models.DateTimeField(auto_now=True,null=False,verbose_name="维修时间")            #维修时间
    def __str__(self):
        return self.customer.cus_name + " " + self.car.car_id + " " + self.repair_time
    class Meta:
        db_table = 'repair_info'
        verbose_name = "维修记录"
        verbose_name_plural = verbose_name
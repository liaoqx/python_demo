from django.contrib import admin
from .models import ErrorsInfo,CustomersInfo,EmployeesInfo,CarsInfo,CarComponentsInfo,UserCarsInfo,RepairInfo

# Register your models here.
admin.site.register(ErrorsInfo)
admin.site.register(CustomersInfo)
admin.site.register(EmployeesInfo)
admin.site.register(CarsInfo)
admin.site.register(CarComponentsInfo)
admin.site.register(UserCarsInfo)
admin.site.register(RepairInfo)
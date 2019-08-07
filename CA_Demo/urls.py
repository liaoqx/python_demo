from django.urls import path,include
import CA_Demo.views
urlpatterns=[
    path('index',CA_Demo.views.index),
    path('login',CA_Demo.views.login)
]
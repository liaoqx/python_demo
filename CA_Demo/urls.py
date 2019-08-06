from django.urls import path,include
import CA_Demo.views
urlpatterns=[
    path('hello_world',CA_Demo.views.hello_world)
]
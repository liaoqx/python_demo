from django import forms
#_*_ coding:utf-8 _*_
class LoginForm(forms.Form):
    username = forms.CharField(required=True,error_messages={'required':u'用户名不能为空'},strip=True)
    password = forms.CharField(widget=forms.PasswordInput(),min_length=6,max_length=16,required=True,strip=True,error_messages={'required':u'密码必须在6-16位'})

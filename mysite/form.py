from  django import forms
from django.contrib.auth import authenticate
# 导入用户模型
from django.contrib.auth.models import User

# 登录, 表单
class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',widget=forms.TextInput(
                                attrs={'class': 'form-control', 'placeholder':'请输入密码'})) 
    # 修改成密文 
    password = forms.CharField(label='密码', widget=forms.PasswordInput(
                                attrs={'class': 'form-control', 'placeholder':'请输入密码'}))

    # 进行数据清洗, 
    def clean(self):
        username=self.cleaned_data['username']
        password=self.cleaned_data['password']
        # 与后台进行,验证
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

# 注册 表单
class RegForm(forms.Form):

    username = forms.CharField(label='用户名', max_length=30, min_length=3, widget=forms.TextInput(
                              attrs={'class': 'form-control', 'placeholder':'请输入3-30位的用户名'})) 

    email = forms.EmailField(label='邮箱',widget=forms.EmailInput(
                                attrs={'class': 'form-control', 'placeholder':'请输入邮箱'})) 

    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput( 
                              attrs={'class': 'form-control', 'placeholder':'请输入密码'}))

    password_again = forms.CharField(label='请再输入一次密码',min_length=6, widget=forms.PasswordInput(
                                attrs={'class': 'form-control', 'placeholder':'请再输入一次密码'}))
    #   验证用户
    def clean_username(self):
        username=self.cleaned_data['username']
        #   验证用户是否存在
        if User.objects.filter(username=username).count() > 0:
            # 抛出错误
            raise   forms.ValidationError('用户名已存在')
        else:
            return username
    #   验证邮箱
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError('邮箱已存在')
        else:
            return email
    def clean_password_again(self):
        password_again=self.cleaned_data['password_again']
        if self.cleaned_data['password'] != password_again:
            raise forms.ValidationError('两次密码不一致')
        else:
            return password_again






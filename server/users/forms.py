from captcha.fields import CaptchaField
from django.forms import ModelForm
from django import forms
from .models import user_account

class RegisterForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        max_length=128,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'username'
        })
    )
    password = forms.CharField(
        label='密码',
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'password'
        })
    )
    password1 = forms.CharField(
        label='确认密码',
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'password again'
        })
    )

    phone = forms.CharField(
        label='手机号',
        max_length=128,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'phone'
        })
    )
    email = forms.EmailField(
        label='邮箱',
        max_length=128,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email'
        })
    )
    captcha = CaptchaField(
        label='验证码',
        error_messages={'invalid': '验证码输入有误'})

class LoginForm(forms.Form):
    # username = forms.CharField(
    #     label='用户名',
    #     max_length=128,
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'username'
    #     })
    # )
    email = forms.EmailField(
        label='邮箱',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'email'
        })
    )
    password = forms.CharField(
        label='密码',
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'password'
        })
    )

class addForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        max_length=128,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'username'
        })
    )
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email'
        })
    )
    password = forms.CharField(
        label='密码',
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'password'
        })
    )
    password1 = forms.CharField(
        label='确认密码',
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'password again'
        })
    )
# class add_upForm(forms.Form):
#     username = forms.CharField(
#         label='用户名',
#         max_length=128,
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'username'
#         })
#     )
#     phone = forms.CharField(
#         label='手机号',
#         max_length=128,
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'phone'
#         })
#     )
#     email = forms.EmailField(
#         label='邮箱',
#         widget=forms.EmailInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'email'
#         })
#     )
#     password = forms.CharField(
#         label='密码',
#         max_length=128,
#         widget=forms.PasswordInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'password'
#         })
#     )
#     password1 = forms.CharField(
#         label='确认密码',
#         max_length=128,
#         widget=forms.PasswordInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'password again'
#         })
#     )


#     sex = forms.CharField(
#         label='性别',
#         max_length=128,
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'sex'
#         })
#     )
#     birthday = forms.DateField(
#         label='邮箱',
#         widget=forms.DateInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'birthday'
#         })
#     )
#     introduction = forms.CharField(
#         label='自我描述',
#         max_length=128,
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'introduction'
#         })
#     )
#     photo = forms.ImageField(
#         label='头像',
#         widget=forms.FileInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'phone'
#         })
#     )




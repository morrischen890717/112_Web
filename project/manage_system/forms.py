from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput()
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput()
    )
# class LoginForm(forms.Form):
#     username = forms.CharField(label='帳號', max_length=10)
#     password = forms.CharField(label='密碼', widget=forms.PasswordInput())
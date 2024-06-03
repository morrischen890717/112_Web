from django import forms
from .models import Event

class LoginForm(forms.Form):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '請輸入帳號'
        })
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '請輸入密碼'
        })
    )
# class LoginForm(forms.Form):
#     username = forms.CharField(label='帳號', max_length=10)
#     password = forms.CharField(label='密碼', widget=forms.PasswordInput())

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['eventName', 'eventDateTime', 'max_limit']
        labels = {
            'eventName': '活動名稱',
            'eventDateTime': '活動時間',
            'max_limit': '人數上限',
        }
        widgets = {
            'eventName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入活動名稱'}),
            'eventDateTime': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'max_limit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '請輸入活動人數上限'}),
        }
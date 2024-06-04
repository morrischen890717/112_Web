from django import forms
from .models import Event
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(
        label="使用者名稱",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '請輸入使用者名稱'
        })
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '請輸入密碼'
        })
    )

class RegisterForm(UserCreationForm): # UserCreationForm 會自帶 password
    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'請輸入使用者名稱'}), 
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'請輸入電子信箱'}),
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '請輸入密碼'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '請再輸入密碼一次'})

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
            'eventDateTime': forms.DateInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'max_limit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '請輸入活動人數上限'}),
        }
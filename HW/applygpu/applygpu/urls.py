"""
URL configuration for applygpu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mainsite.views import homepage, showNews, applyRule, applyStatus, registerPage, register, loginPage, login, simple_mail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage),
    path('news/<slug:slug>/', showNews),
    path('apply_rule/', applyRule),
    path('apply_status/', applyStatus),
    path('register_page/', registerPage),
    path('register/', register),
    path('login_page', loginPage),
    path('login', login),
    path('mail', simple_mail),
]

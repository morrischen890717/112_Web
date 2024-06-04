"""
URL configuration for project project.

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
from manage_system.views import homepage, eventPage, participantPage, eventInvitePage, \
allowlistPage, invitePage, welcomePage, sign_in, register, log_out, createEvent, saveNewEvent, deleteEvent

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', sign_in),
    path('base/', homepage),
    path("eventPage", eventPage),
    path("eventPage/<str:eventName>", participantPage, name='participantPage'),
    path("eventInvitePage/<str:eventName>", eventInvitePage, name='eventInvitePage'),
    path('register/', register),
    path('allowlistPage', allowlistPage),
    path('invitePage/<str:uniqueId>', invitePage),
    path('welcomePage/<str:uniqueId>', welcomePage, name='welcomePage'),
    path('login/', sign_in),
    path('logout', log_out, name='Logout'),
    path('createEvent', createEvent),
    path('createEvent/saveNewEvent', saveNewEvent),
    path('deleteEvent/<str:id>', deleteEvent),
]

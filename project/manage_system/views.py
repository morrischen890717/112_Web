from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Event, User
from .forms import LoginForm, EventForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .api.backend import initializeEventSetting, getAllParticipant, acceptSpecifiedParticipant, getAllAllowlist, \
acceptAllowlistParticipant, decodeUniqueId, insertSpecifiedParticipantData, sendSpecifiedParticipantInvite

# Create your views here.
def homepage(request):
    return render(request, 'base.html')

@login_required(login_url='login/')
def eventPage(request):
    # try:
    #     event_name = request.GET['event-name']
    #     sheet_id, draft_id = initializeEventSetting(event_name)
    # except:
    #     event_name, sheetId, draftId = None, None, None
    #     print("The event is not created because the corresponding sheet and draft cannot be found.")

    # if event_name != None:            
    #     Event.objects.create(eventName=event_name, sheetId=sheet_id, draftId=draft_id)
    events = Event.objects.all()
    return render(request, 'eventPage.html', locals())

@login_required(login_url='login/')
def participantPage(request, eventName):
    
    event = Event.objects.get(eventName=eventName)

    send_allowlist = request.GET.get('send_allowlist')
    if send_allowlist: acceptAllowlistParticipant(event.sheetId, event.draftId, '已錄取（白名單）')

    participants_status = request.GET.getlist('participants_status')
    row_participants_accept  = [ index+2 for index, participant_status in enumerate(participants_status) 
                                if participant_status == 'accept']

    if row_participants_accept: 
        acceptSpecifiedParticipant(event.sheetId, event.draftId, row_participants_accept, '已錄取')

    participants = getAllParticipant(event.sheetId)

    return render(request, 'participantPage.html', locals())

@login_required(login_url='login/')
def eventInvitePage(request, eventName):

    participants_status = request.GET.getlist('invite_status')
    row_participants_invite  = [ index+2 for index, participant_status in enumerate(participants_status) 
                                if participant_status == 'invite']

    if row_participants_invite: 
        sendSpecifiedParticipantInvite(eventName, row_participants_invite)

    participants = getAllAllowlist()
    return render(request, 'eventInvitePage.html', locals())

@login_required(login_url='login/')
def allowlistPage(request):

    allow_participants = getAllAllowlist()
    return render(request, 'allowlistPage.html', locals())

def invitePage(request, uniqueId):
    participant_info = decodeUniqueId(uniqueId)

    return render(request, 'linkInvitePage.html', locals())

def welcomePage(request, uniqueId):
    participate = request.GET.get('participate')

    participant_info = decodeUniqueId(uniqueId)
    if participate:
        event = Event.objects.get(eventName=participant_info[0])
        sheet_id = event.sheetId
        insertSpecifiedParticipantData(sheet_id, participant_info, '已錄取（邀請）')

    return render(request, 'linkWelcomePage.html', locals())

#註冊
def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')  #重新導向到登入畫面
    context = {
        'form': form
    }
    return render(request, 'register.html', context)

#登入
def sign_in(request):
    if request.method == 'POST':
        Login_form = LoginForm(request.POST)
        if Login_form.is_valid():
            login_username = request.POST.get("username")
            login_password = request.POST.get("password")
            user = authenticate(request, username=login_username, password=login_password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('base/')
                else:
                    messages.add_message(request, messages.WARNING, "帳號尚未啟用")
            else:
                messages.add_message(request, messages.WARNING, "登入失敗")
        else:
            messages.add_message(request, messages.INFO, "檢查輸入內容")
    else:
        Login_form = LoginForm()
    return render(request, 'login.html', locals())

def log_out(request):
    logout(request)
    messages.add_message(request, messages.INFO, "成功登出")
    return redirect('/') 

@login_required(login_url='login/')
def createEvent(request):
    form = EventForm()
    return render(request, 'createEvent.html', locals())

@login_required(login_url='login/')
def saveNewEvent(request):
    form = EventForm(request.POST)
    if form.is_valid():
        try:
            eventName = form.cleaned_data['eventName']
            sheet_id, draft_id = initializeEventSetting(eventName)
        except:
            eventName, sheetId, draftId = None, None, None
            print("The event is not created because the corresponding sheet and draft cannot be found.")
    if eventName != None:            
        form.save()
        event = Event.objects.get(eventName=eventName)
        event.sheetId, event.draftId= sheet_id, draft_id
        event.save()

    return redirect('/eventPage')

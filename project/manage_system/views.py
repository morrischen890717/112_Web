from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Event, User
from .forms import LoginForm, RegisterForm, EventForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .api.backend import initializeEventSetting, getAllParticipant, acceptSpecifiedParticipant, getAllAllowlist, \
acceptAllowlistParticipant, decodeUniqueId, insertSpecifiedParticipantData, sendSpecifiedParticipantInvite, \
getAllEventInfos, insertMultiSpecifiedParticipantData


# Create your views here.

def homepage(request):
    return render(request, 'base.html')

@login_required(login_url='login/')
def eventPage(request):

    events = Event.objects.all()
    sheet_ids = [ event.sheetId for event in events ]
    accept_counts, total_counts = getAllEventInfos(sheet_ids)
    
    events_and_counts = zip(events, accept_counts, total_counts)

    return render(request, 'eventPage.html', locals())

@login_required(login_url='login/')
def participantPage(request, eventName):
    
    event = Event.objects.get(eventName=eventName)

    send_allowlist = request.GET.get('send_allowlist')
    if send_allowlist: acceptAllowlistParticipant(event.sheetId, event.draftId, '錄取-白名單')

    participants_status = request.GET.getlist('participants_status')
    row_participants_accept  = [ index+2 for index, participant_status in enumerate(participants_status) 
                                if participant_status == 'accept']

    if row_participants_accept: 
        acceptSpecifiedParticipant(event.sheetId, event.draftId, row_participants_accept, '錄取')

    row_participants_accept  = [ index+2 for index, participant_status in enumerate(participants_status) 
                                if participant_status == 'allowlist']
    
    if row_participants_accept:
        insertMultiSpecifiedParticipantData(event.sheetId, row_participants_accept)

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
        insertSpecifiedParticipantData(sheet_id, participant_info, '錄取-邀請')

    return render(request, 'linkWelcomePage.html', locals())

#註冊
def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/login')
    # if request.method == "POST":
    #     form = UserCreationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('/login')  #重新導向到登入畫面
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
                    return redirect('/eventPage')
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
    if eventName:            
        event = form.save(commit=False)
        event.createUser, event.sheetId, event.draftId = request.user, sheet_id, draft_id
        event.save()
        messages.add_message(request, messages.INFO, "新增活動成功。")
    else:
        messages.add_message(request, messages.ERROR, "無法新增活動。")
    return redirect('/eventPage')

@login_required(login_url='login/')
def deleteEvent(request, id):
    try:
        event = Event.objects.get(id=id)
    except:
        event = None
    if event:
        event.delete()
        messages.add_message(request, messages.INFO, "成功刪除活動。")
    else:
        messages.add_message(request, messages.ERROR, "該活動不存在。")
    return redirect('/eventPage')



from django.shortcuts import render
from .models import Event
from .api.backend import initializeEventSetting, getAllParticipant, acceptSpecifiedParticipant

# Create your views here.
def homepage(request):
    return render(request, 'base.html')

def eventPage(request):
    try:
        event_name = request.GET['event-name']
        sheet_id, draft_id = initializeEventSetting(event_name)
    except:
        event_name, sheetId, draftId = None, None, None
        print("The event is not created because the corresponding sheet and draft cannot be found.")

    if event_name != None:            
        Event.objects.create(eventName=event_name, sheetId=sheet_id, draftId=draft_id)

    events = Event.objects.all()
    return render(request, 'eventPage.html', locals())

def participantPage(request, eventName):
    
    participants_status = request.GET.getlist('participants_status')
    row_participants_accept  = [ index+2 for index, participant_status in enumerate(participants_status) 
                                if participant_status == 'accept']

    event = Event.objects.get(eventName=eventName)

    if row_participants_accept: 
        acceptSpecifiedParticipant(event.sheetId, event.draftId, row_participants_accept, 'Send!')

    participants = getAllParticipant(event.sheetId)

    return render(request, 'participantPage.html', locals())
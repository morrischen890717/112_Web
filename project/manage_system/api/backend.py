from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .google_cloud import returnUserCred, querySheetIdandDraftId, returnSpecifiedFileId, \
insertFirstColumninSheet, getSpecifiedParticipantInfo, \
sendSpecifiedParticipantGmail, updateSpecifiedParticipantStatus, insertFirstRowinSheet, updateSpecifiedParticipantData, \
generateUniqueLinks, sendUniqueInviteLinks
import base64

########## Event Overview Page ##########

def getAllEventInfos(sheet_ids: list):

  creds = returnUserCred()
  service = build("sheets", "v4", credentials=creds)

  counts = [None] * len(sheet_ids)
  for i, sheet_id in enumerate(sheet_ids):
    try:
      # Get Sheet Content in First File
      result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=f"{sheet_id}", range="A2:A")
        .execute()
      ).get('values')
      
      if result: counts[i] = len([row for row in result if row])
      else: counts[i] = 0

    except HttpError as error:
      # TODO(developer) - Handle errors from drive API.
      print(f"An error occurred: {error}")

  return counts

# When user create new event
def initializeEventSetting(event_name: str):

  print(event_name)
  sheet_id, draft_id = querySheetIdandDraftId(event_name)
  insertFirstColumninSheet(sheet_id)

  # print(f'sheet_id: {sheet_id}')
  # print(f'draft_id: {draft_id}')
  return sheet_id, draft_id
  
  # TODO: Write sheet_id and draft_id to the Event model

########## Specified Event Page (/event.slug) ##########

# Specified event page demonstrate
def getAllParticipant(sheet_id: str):

  creds = returnUserCred()
  # fileId = returnSpecifiedFileId()

  try:
    # Get Sheet Content in First File
    service = build("sheets", "v4", credentials=creds)
    result = (
      service.spreadsheets()
      .values()
      .get(spreadsheetId=f"{sheet_id}", range="A2:C")
      .execute()
    ).get('values')

    return result

  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")

# When user accept specified participant
def acceptSpecifiedParticipant(sheet_id: str, draft_id: str, row_participants: list, status: str):

  participant_infos = getSpecifiedParticipantInfo(sheet_id, row_participants)
  participant_emails = [participant_info['Email'] for participant_info in participant_infos]
 
  sendSpecifiedParticipantGmail(draft_id, participant_emails)
  updateSpecifiedParticipantStatus(sheet_id, row_participants, status)

# When user accept allowlist participant
def acceptAllowlistParticipant(sheet_id: str, draft_id: str, status: str):
  
  creds = returnUserCred()
  # fileId_event = returnSpecifiedFileId()

  # TODO: Retrieve the fileId from the # model instead of searching with the Google API
  fileId_allow = returnSpecifiedFileId('允許名單')

  try:
    # Get Sheet Content in First File
    service = build("sheets", "v4", credentials=creds)
    event_participants = (
      service.spreadsheets()
      .values()
      .get(spreadsheetId=f"{sheet_id}", range="C2:C")
      .execute()
    ).get('values')

    allow_participants = (
      service.spreadsheets()
      .values()
      .get(spreadsheetId=f"{fileId_allow}", range="C2:C")
      .execute()
    ).get('values')

  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")

  event_participant_emails = [event_participant[0] for event_participant in event_participants]
  allow_participant_emails = [allow_participant[0] for allow_participant in allow_participants]

  print(event_participant_emails)

  # accept_emails = set(event_participant_emails) & set(allow_participant_emails)
  accept_rows = [index+2 for index, event_participant_email in enumerate(event_participant_emails) 
                  if event_participant_email in allow_participant_emails]
  
  acceptSpecifiedParticipant(sheet_id, draft_id, accept_rows, status)

def sendSpecifiedParticipantInvite(event_name:str, row_participants: list):

  unique_links = generateUniqueLinks(event_name, row_participants)
  sendUniqueInviteLinks (event_name, row_participants, unique_links)

def insertMultiSpecifiedParticipantData(sheet_id: str, row_participants: list):

  participant_infos = getSpecifiedParticipantInfo(sheet_id, row_participants)
  
  for participant_info in participant_infos:
    insertSpecifiedParticipantData(returnSpecifiedFileId(), [0, participant_info['Name'], participant_info['Email']], '-')

########## Allow List Page ##########

# Allow List Page demonstrate
def getAllAllowlist():

  creds = returnUserCred()
  fileId = returnSpecifiedFileId('允許名單')

  try:
    # Get Sheet Content in First File
    service = build("sheets", "v4", credentials=creds)
    result = (
      service.spreadsheets()
      .values()
      .get(spreadsheetId=f"{fileId}", range="B2:C")
      .execute()
    ).get('values')

    return result

  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")

def decodeUniqueId(unique_id: str):
  participant_info = base64.urlsafe_b64decode(unique_id.encode('utf-8')).decode('utf-8')
  participant_info = participant_info.split('|')

  return participant_info

########## Welcome Page ##########
def insertSpecifiedParticipantData(sheet_id: str, participant_info: list, status: str):
  insertFirstRowinSheet(sheet_id)
  updateSpecifiedParticipantData(sheet_id, participant_info, status)
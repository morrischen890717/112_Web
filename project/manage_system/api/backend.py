from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .google_cloud import returnUserCred, querySheetIdandDraftId, returnSpecifiedFileId, insertFirstColumninSheet, getSpecifiedParticipantInfo, sendSpecifiedParticipantGmail, updateSpecifiedParticipantStatus

########## Event Overview Page ##########

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

# When user accept specified participant (Add parameter event.slug: int)
def acceptSpecifiedParticipant(sheet_id: str, draft_id: str, row_participants: list, status: str):

  participant_infos = getSpecifiedParticipantInfo(sheet_id, row_participants)
  participant_emails = [participant_info['Email'] for participant_info in participant_infos]
 
  sendSpecifiedParticipantGmail(draft_id, participant_emails)
  updateSpecifiedParticipantStatus(sheet_id, row_participants, status)

# When user accept allowlist participant (Add parameter event.slug: int)
def acceptAllowlistParticipant(sheet_id: str, draft_id: str, status: str):
  
  creds = returnUserCred()
  fileId_event = returnSpecifiedFileId()

  # TODO: Retrieve the fileId from the # model instead of searching with the Google API
  fileId_allow = returnSpecifiedFileId('允許名單')

  try:
    # Get Sheet Content in First File
    service = build("sheets", "v4", credentials=creds)
    event_participants = (
      service.spreadsheets()
      .values()
      .get(spreadsheetId=f"{fileId_event}", range="C2:C")
      .execute()
    ).get('values')

    allow_participants = (
      service.spreadsheets()
      .values()
      .get(spreadsheetId=f"{fileId_allow}", range="B2:B")
      .execute()
    ).get('values')

  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")

  event_participant_emails = [event_participant[0] for event_participant in event_participants]
  allow_participant_emails = [allow_participant[0] for allow_participant in allow_participants]

  # accept_emails = set(event_participant_emails) & set(allow_participant_emails)
  accept_rows = [index+2 for index, event_participant_email in enumerate(event_participant_emails) 
                  if event_participant_email in allow_participant_emails]
  
  acceptSpecifiedParticipant(sheet_id, draft_id, accept_rows, '饗食天堂！')

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
      .get(spreadsheetId=f"{fileId}", range="A2:B")
      .execute()
    ).get('values')

    return result

  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")

########## Allow List Page ##########
# def 
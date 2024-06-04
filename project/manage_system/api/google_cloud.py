#https://developers.google.com/drive/api/quickstart/python?hl=zh-tw

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import base64
from email.message import EmailMessage
from email.mime.text import MIMEText
from email import message_from_bytes

import json

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive", "https://mail.google.com/"]

#Google Auth
def returnUserCred():
  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("manage_system/google_creds/token.json"):
    creds = Credentials.from_authorized_user_file("manage_system/google_creds/token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "manage_system/google_creds/credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=8080)
    # Save the credentials for the next run
    with open("manage_system/google_creds/token.json", "w") as token:
      token.write(creds.to_json())
  return creds

#Google Drive
# TODO: Retrieve the fileId from the Event model instead of searching with the Google API (Add parameter event.slug: int)
def returnSpecifiedFileId(event_name: str = '0615'):
  
  creds = returnUserCred()
  try:
    service = build("drive", "v3", credentials=creds)

    # Get First File in Directory ID
    sheetId = (
      service.files()
      .list(q=f"name contains '{event_name}'", fields="files(id, name)")
      .execute()
    ).get("files")[0].get("id")

    return sheetId
  
  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")

#Google Drive
#backend_api: initializeEventSetting
def querySheetIdandDraftId(event_name: str):
  creds = returnUserCred()
  try:
    service = build("drive", "v3", credentials=creds)

    sheetId = (
      service.files()
      .list(q=f"name contains '{event_name}'", fields="files(id, name)")
      .execute()
    ).get("files")[0].get("id")

    service = build("gmail", "v1", credentials=creds)

    # Get Draft ID by Query
    draftId = (
      service.users().drafts()
      .list(userId = 'me', q = f"subject:({event_name})")
      .execute()
    ).get("drafts")[0].get("id")

    return sheetId, draftId

  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")

#Google Sheet
#backend_api: initializeEventSetting
def insertFirstColumninSheet(sheet_id: str):

  creds = returnUserCred()

  request_body = {
    "requests":[{
      "insertDimension": {
        "range": {
          "sheetId": 0,
          "dimension": "COLUMNS",
          "startIndex": 0,
          "endIndex": 1
        },
      "inheritFromBefore": False
      }
    }]
  }

  try:
    service = build("sheets", "v4", credentials=creds)
    result = (
      service.spreadsheets()
      .batchUpdate(spreadsheetId=f"{sheet_id}", body = request_body)
      .execute()
    )

  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None

#Google Sheet
#backend_api: acceptSpecifiedParticipant
def getSpecifiedParticipantInfo(sheet_id: str, row_participants: list) -> dict:
  
  creds = returnUserCred()
  # fileId = returnSpecifiedFileId()

  ranges = [f"A{int(row)}:D{int(row)}" for row in row_participants]

  try:
    service = build("sheets", "v4", credentials=creds)

    result = (
      service.spreadsheets()
      .values()
      .batchGet(spreadsheetId=sheet_id, ranges=ranges)
      .execute()
    ).get("valueRanges")

    participant_infos = [{ "Name": f"{result[index].get('values')[0][1]}", 
              "Email": f"{result[index].get('values')[0][2]}"} for index in range(len(result))]

    # participant_infos = [{"Email": f"{result[index].get('values')[0][3]}"} for index in range(len(result))]

    return participant_infos

  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None

#Google Sheet
#backend_api: acceptSpecifiedParticipant
def updateSpecifiedParticipantStatus(sheet_id: str, row_participants: list, status: str):

  creds = returnUserCred()
  # fileId = returnSpecifiedFileId()

  try:
    service = build("sheets", "v4", credentials=creds)

    data = [{"range": f"A{int(row_number)}",  "values": [[f"{status}"]]} for row_number in row_participants]

    body = {
        "valueInputOption": "USER_ENTERED",
        "data": data
    }

    result = (
        service.spreadsheets()
        .values()
        .batchUpdate(spreadsheetId=sheet_id, body=body)
        .execute()
    )
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error

def insertFirstRowinSheet(sheet_id: str):
  
  creds = returnUserCred()

  request_body = {
    "requests":[{
      "insertDimension": {
        "range": {
          "sheetId": 0,
          "dimension": "ROWS",
          "startIndex": 1,
          "endIndex": 2
        },
      "inheritFromBefore": False
      }
    }]
  }

  try:
    service = build("sheets", "v4", credentials=creds)
    result = (
      service.spreadsheets()
      .batchUpdate(spreadsheetId=f"{sheet_id}", body = request_body)
      .execute()
    )
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error

def updateSpecifiedParticipantData(sheet_id: str, participant_info: list, status: str):
  creds = returnUserCred()
  
  values = [
    [f'{status}', f'{participant_info[1]}', f'{participant_info[2]}'],
  ]

  data = {
      'range': '2:2',
      'majorDimension': 'ROWS',
      'values': values
  }

  service = build("sheets", "v4", credentials=creds)

  service.spreadsheets().values().update(
      spreadsheetId=sheet_id,
      range='2:2',
      valueInputOption='RAW',
      body=data
  ).execute()

#Gmail
#backend_api: acceptSpecifiedParticipant
# TODO: Retrieve the draftId from the Event model
def sendSpecifiedParticipantGmail(draft_id: str, participant_emails: list):

  creds = returnUserCred()

  try:
    service = build("gmail", "v1", credentials=creds)

    # Get Draft ID by Query
    # draftId = (
    #   service.users().drafts()
    #   .list(userId = 'me', q = "subject:(動物方程式)")
    #   .execute()
    # ).get("drafts")[0].get("id")

    # Get Draft Content
    draft = (
      service.users().drafts()
      .get(userId = 'me', id = f"{draft_id}", format = 'raw')
      .execute()
    ).get("message").get("raw")

    participant_emails = ", ".join(str(participant_email) for participant_email in participant_emails)

    # 解碼並解析郵件內容
    # draft = MIMEText(base64.urlsafe_b64decode(draft.encode('ASCII')).decode('utf-8'))
    draft = message_from_bytes(base64.urlsafe_b64decode(draft.encode('ASCII')))

    # 修改收件人
    # draft.replace_header('Bcc', "ameliahuang0105@gmail.com")
    draft['Bcc'] = participant_emails

    # draft = base64.urlsafe_b64encode(draft.encode()).decode()
    draft = base64.urlsafe_b64encode(draft.as_bytes()).decode('ASCII')

    # Send Email to Recipient
    draft = (
      service.users().messages()
      .send(userId = 'me', body={"raw": draft})
      .execute()
    )

  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None
  return creds

def generateUniqueLinks(event_name: str, row_participants: list):

  creds = returnUserCred()
  fileId = returnSpecifiedFileId('允許名單')

  participant_infos = getSpecifiedParticipantInfo(fileId, row_participants)

  unique_invite_links = [None] * len(participant_infos)
  
  for i, participant_info in enumerate(participant_infos):
    participant_info = f"{event_name}|{participant_info['Name']}|{participant_info['Email']}"
    participant_info = base64.urlsafe_b64encode(participant_info.encode('utf-8')).decode('utf-8')
    unique_invite_links[i] = f'http://127.0.0.1:8000/invitePage/{participant_info}'

  return unique_invite_links

def sendUniqueInviteLinks(event_name:str, row_participants: list, unique_invite_links: list):
  """Create and send an email message
  Print the returned  message id
  Returns: Message object, including message id

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  creds = returnUserCred()
  fileId = returnSpecifiedFileId('允許名單')

  try:
    service = build("gmail", "v1", credentials=creds)
    message = EmailMessage()
    participant_infos = getSpecifiedParticipantInfo(fileId, row_participants)

    for participant_info, unique_invite_link in zip(participant_infos, unique_invite_links):

      message.set_content(f"Hi, {participant_info['Name']}: {unique_invite_link}")

      message["To"] = f"{participant_info['Email']}"
      # message["From"] = "gduser2@workspacesamples.dev"
      message["Subject"] = f"邀請您參加{event_name}"

      # encoded message
      encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

      create_message = {"raw": encoded_message}
      # pylint: disable=E1101
      send_message = (
          service.users()
          .messages()
          .send(userId="me", body=create_message)
          .execute()
      )
      print(f'Message Id: {send_message["id"]}')

  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None
  return send_message

if __name__ == "__main__":
  None
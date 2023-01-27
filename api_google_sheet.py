from pprint import pprint
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

import httplib2
import apiclient


# Файл ключ, полученный в Google Developer Console
CREDENTIALS_FILE = 'google_cr.json'
# ID Google Sheets документа (можно взять из его URL)
SPREADSHEET_ID = '1Y_SZ2z8Wn3RdwwnROy4wedEAuB4t1bJOY6Dlv6SRjpA'


def connect_to_file():
    # Авторизуемся и получаем service — экземпляр доступа к API
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
    return service


def get_data_from_sheets(service):
    # Пример чтения файла
    values = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='A1:E10',
        majorDimension='COLUMNS'
    ).execute()
    pprint(values)
def push_data_to_sheets(service):
    # Пример записи в файл
    values = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range = "Лист1!A1:A",
        body= {
            "majorDimension": "COLUMNS",
            "values": [[str(datetime.now())], ["Ссылка"]]
                # {"range": "Лист1!A5:A",
                #  "majorDimension": "COLUMNS",
                #  "values": [["This is D5", "This is D6"], ["This is E5", "=5+5"]]}

        },
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS"
    ).execute()


#insertDataOption=INSERT_ROWS,
# list = [["valuea1"], ["valuea2"], ["valuea3"]]
# resource = {
#   "majorDimension": "ROWS",
#   "values": list
# }
# spreadsheetId = "### spreadsheet ID"
# range = "Sheet1!A:A";
#
# service.spreadsheets().values().append(
#   spreadsheetId=spreadsheetId,
#   range=range,
#   body=resource,
#   valueInputOption="USER_ENTERED"
# ).execute()
from google.oauth2 import service_account
from googleapiclient.discovery import build
from os import getenv
from ..commons import read_json

def get_calendar_list():
    return read_json(getenv('g_calendar_settings'))
    
def get_secret_path():
    return getenv('gapi_secret_path')

class google_calendar:
    __slots__='service','scopes'
    def __init__(self,secret_path:str,api_version:str='v3'):
        self.scopes=['https://www.googleapis.com/auth/calendar']
        credentials=service_account.Credentials.from_service_account_file(filename=secret_path,scopes=self.scopes)
        self.service=build('calendar',api_version,credentials=credentials)
        
    def calendar_list(self):
        return self.service.calendarList().list().execute()
    
    def add_calendar(self,calendar_id:str):
        return self.service.calendarList().insert(body={'id':calendar_id}).execute()
        
#file=r'C:\Users\ivolochkov\YandexDisk\calendar.json'
    
#obj=google_calendar(file)   

#from pprint import pprint
#pprint(obj.calendarcls_list())
#print(read_json(file))

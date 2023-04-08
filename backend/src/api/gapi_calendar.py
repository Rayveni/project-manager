from google.oauth2 import service_account
from googleapiclient.discovery import build
from os import getenv
from ..commons import read_json

def get_calendar_list():
    return read_json(getenv('g_calendar_settings'))
    
def get_secret_path():
    return getenv('gapi_secret_path')

def format_event(event:dict,event_color:str=None)->dict:
    if event['start'].get('dateTime') is None:
        start,end,allDay=event['start']['date'],event['end']['date'],True
    else:
         start,end,allDay=event['start']['dateTime'],event['end']['dateTime'],False
        
    res={
        #'id':,String. A unique identifier of an event. Useful for getEventById.
        #'groupId':,#String. Events that share a groupId will be dragged and resized together automatically.
        'allDay':allDay,#Boolean (true or false). Determines if the event is shown in the “all-day” section of relevant views. In addition, if true the time text is not displayed with the event.
        'start':start,#Date object that obeys the current timeZone. When an event begins.
        'end':end,#Date object that obeys the current timeZone. When an event ends. It could be null if an end wasn’t specified.
        #Note: This value is exclusive. For example, an event with the end of 2018-09-03 will appear to span through 2018-09-02 but end before the start of 2018-09-03. See how events are are parsed from a plain object for further details.
        #'startStr':,An ISO8601 string representation of the start date. If the event is all-day, there will not be a time part.
        #'endStr':,An ISO8601 string representation of the end date. If the event is all-day, there will not be a time part.
        'title':event.get('summary',''),#String. The text that will appear on an event.
        'url':event['htmlLink'],#String. A URL that will be visited when this event is clicked by the user. For more information on controlling this behavior, see the eventClick callback.
        #'classNames':,An array of strings like [ 'myclass1', myclass2' ]. Determines which HTML classNames will be attached to the rendered event.
        #'editable':,Boolean (true or false) or null. The value overriding the editable setting for this specific event.
        #'startEditable':,Boolean (true or false) or null. The value overriding the eventStartEditable setting for this specific event.
        #'durationEditable':,Boolean (true or false) or null. The value overriding the eventDurationEditable setting for this specific event.
        #'resourceEditable':,Boolean (true or false) or null. The value overriding the eventResourceEditable setting for this specific event.
        #'display':,The rendering type of this event. Can be 'auto', 'block', 'list-item', 'background', 'inverse-background', or 'none'. See eventDisplay.
        #'overlap':,The value overriding the eventOverlap setting for this specific event. If false, prevents this event from being dragged/resized over other events. Also prevents other events from being dragged/resized over this event. Does not accept a function.
        #'constraint':,The eventConstraint override for this specific event.
        #'backgroundColor':,The eventBackgroundColor override for this specific event.
        #'borderColor':,The eventBorderColor override for this specific event.
        #'textColor':,The eventTextColor override for this specific event.
        #'extendedProps':,A plain object holding miscellaneous other properties specified during parsing. Receives properties in the explicitly given extendedProps hash as well as other non-standard properties.
        #'source':,A reference to the Event Source this event came from. If the event was added dynamically via addEvent, and the source parameter was not specified, this value will be null.
        'description': event.get('description')     
    }
    if event_color:
        res['color']=event_color
    return res

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

    def events(self,calendar_id:str,start_date:str=None,end_date:str=None):
        """
        https://developers.google.com/calendar/api/v3/reference/events/list
        timeMin:Lower bound (exclusive) for an event's end time to filter by. 
                Optional. The default is not to filter by end time. 
                Must be an RFC3339 timestamp with mandatory time zone offset, 
                for example, 2011-06-03T10:00:00-07:00, 2011-06-03T10:00:00Z. 
                Milliseconds may be provided but are ignored. 
                If timeMax is set, timeMin must be smaller than timeMax.
        """     
        page_token,res_events = None,[]
        while True:
            events = self.service.events().list(calendarId=calendar_id, pageToken=page_token,timeMin=start_date,timeMax=end_date).execute()
            res_events+=events.get('items')
            page_token = events.get('nextPageToken')
            if not page_token:
                 break
        events_info={key:events[key] for key in events if key!='items'}
        return {'events_info':events_info,'events':res_events}
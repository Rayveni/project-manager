from os import path as os_path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
#from googleapiclient.errors import HttpError
# If modifying  scopes, delete the file token.json.
#https://google-api-client-libraries.appspot.com/documentation/tasks/v1/python/latest/index.html

class google_tasks:
    __slots__ = 'tasks_service','secret_store','scopes','maxResults'

    def __init__(self, secret_path: str,secret_store:str, api_version: str = 'v1'):
        self.maxResults=100
        self.scopes,self.secret_store = ['https://www.googleapis.com/auth/tasks'],secret_store
        credentials=self.__auth(secret_path,secret_store,self.scopes)
        self.tasks_service = build('tasks', api_version, credentials=credentials)
        
    def __auth(self,secret_path,secret_store,scopes):
        creds = None
        if os_path.exists(secret_store):
            creds = Credentials.from_authorized_user_file(secret_store, scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(secret_path, scopes)
                creds = flow.run_local_server(port=0)
                with open(secret_store, 'w') as token:
                    token.write(creds.to_json())
        return creds
    
    def _next_page_loop(self,f,nextPageToken:str=None):
        result=f(nextPageToken)
        token=result.get('nextPageToken', None)
        res=result['items']

        while token!=None:
            result=f(token)
            res+=result['items']
            token = result.get('nextPageToken', None)
        return res
    
    def tasklists(self):
        return self.tasks_service.tasklists().list().execute()
    
    def get_tasks(self,tasklist:str="@default",completedMin:str=None):
        """google api reference
                list(tasklist=*, showCompleted=None, dueMin=None, dueMax=None, pageToken=None, updatedMin=None, showDeleted=None, completedMax=None, maxResults=None, completedMin=None, showHidden=None)
                Returns all tasks in the specified task list.

                Args:
                tasklist: string, Task list identifier. (required)
                showCompleted: boolean, Flag indicating whether completed tasks are returned in the result. Optional. The default is True.
                dueMin: string, Lower bound for a task's due date (as a RFC 3339 timestamp) to filter by. Optional. The default is not to filter by due date.
                dueMax: string, Upper bound for a task's due date (as a RFC 3339 timestamp) to filter by. Optional. The default is not to filter by due date.
                pageToken: string, Token specifying the result page to return. Optional.
                updatedMin: string, Lower bound for a task's last modification time (as a RFC 3339 timestamp) to filter by. Optional. The default is not to filter by last modification time.
                showDeleted: boolean, Flag indicating whether deleted tasks are returned in the result. Optional. The default is False.
                completedMax: string, Upper bound for a task's completion date (as a RFC 3339 timestamp) to filter by. Optional. The default is not to filter by completion date.
                maxResults: string, Maximum number of task lists returned on one page. Optional. The default is 20 (max allowed: 100).
                completedMin: string, Lower bound for a task's completion date (as a RFC 3339 timestamp) to filter by. Optional. The default is not to filter by completion date.
                showHidden: boolean, Flag indicating whether hidden tasks are returned in the result. Optional. The default is False.
        """
        f=lambda _token:self.tasks_service.tasks().list(tasklist=tasklist,showHidden=True,
                                                        completedMin=completedMin,maxResults=self.maxResults,pageToken=_token).execute()
        return self._next_page_loop(f)
    
    def insert_task(self,tasklist:str="@default", body=None, parent:str=None, previous:str=None):
        """google api reference
            insert(tasklist=*, body=None, parent=None, previous=None)
            Creates a new task on the specified task list. Fails with HTTP code 403 or 429 after reaching the storage limit of 100,000 tasks per account.

            Args:
            tasklist: string, Task list identifier. (required)
            body: object, The request body.
                The object takes the form of:

            {
                {
                "status": "A String", # Status of the task. This is either "needsAction" or "completed".
                "kind": "tasks#task", # Type of the resource. This is always "tasks#task".
                "updated": "A String", # Last modification time of the task (as a RFC 3339 timestamp).
                "parent": "A String", # Parent task identifier. This field is omitted if it is a top-level task. This field is read-only. Use the "move" method to move the task under a different parent or to the top level.
                "links": [ # Collection of links. This collection is read-only.
                {
                    "type": "A String", # Type of the link, e.g. "email".
                    "link": "A String", # The URL.
                    "description": "A String", # The description. In HTML speak: Everything between <a> and </a>.
                },
                ],
                "title": "A String", # Title of the task.
                "deleted": True or False, # Flag indicating whether the task has been deleted. The default if False.
                "completed": "A String", # Completion date of the task (as a RFC 3339 timestamp). This field is omitted if the task has not been completed.
                "due": "A String", # Due date of the task (as a RFC 3339 timestamp). Optional. The due date only records date information; the time portion of the timestamp is discarded when setting the due date. It isn't possible to read or write the time that a task is due via the API.
                "etag": "A String", # ETag of the resource.
                "notes": "A String", # Notes describing the task. Optional.
                "position": "A String", # String indicating the position of the task among its sibling tasks under the same parent task or at the top level. If this string is greater than another task's corresponding position string according to lexicographical ordering, the task is positioned after the other task under the same parent task (or at the top level). This field is read-only. Use the "move" method to move the task to another position.
                "hidden": True or False, # Flag indicating whether the task is hidden. This is the case if the task had been marked completed when the task list was last cleared. The default is False. This field is read-only.
                "id": "A String", # Task identifier.
                "selfLink": "A String", # URL pointing to this task. Used to retrieve, update, or delete this task.
            }

            parent: string, Parent task identifier. If the task is created at the top level, this parameter is omitted. Optional.
            previous: string, Previous sibling task identifier. If the task is created at the first position among its siblings, this parameter is omitted. Optional.
        """    
        return self.tasks_service.tasks().insert(tasklist=tasklist, body=body,parent=parent,previous=previous).execute()
    
    def __update_task(self,task:str,tasklist:str="@default", body=None):     
        return self.tasks_service.tasks().update(tasklist=tasklist, task=task, body=body).execute()

    def close_task(self,task:str,tasklist:str="@default"):     
        body={'status':'completed','id':task}
        return self.__update_task(tasklist=tasklist, task=task, body=body)
    
    def clear(self,tasklist:str="@default"):  
        """
        clear(tasklist=*)
        Clears all completed tasks from the specified task list. The affected tasks will be marked as 'hidden' and no longer be returned by default when retrieving all tasks for a task list.

        Args:
        tasklist: string, Task list identifier. (required) 
        """      
        return self.tasks_service.tasks().clear(tasklist=tasklist).execute()  
   
    
#gt=google_tasks(r'C:\Users\volochkov\Downloads\tasks_api.json','token2.json')

#print(gt.get_tasks('dFp6bVFHeXZMYjl6MkdtaQ'))
#print(gt.insert_task(tasklist='dFp6bVFHeXZMYjl6MkdtaQ',body={ 'title': 'Test task insert3' }))

#print(gt.close_task('OG9TYnNfZzVUTWxLQWE4bw','dFp6bVFHeXZMYjl6MkdtaQ'))
#print(gt.clear())
#print(gt.get_tasks())

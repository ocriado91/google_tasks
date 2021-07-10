#!/usr/bin/env python3

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

''' Google Task API to retrieve task list 
    and tasks '''

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/tasks.readonly']

class GoogleTasks:
    ''' Google Tasks class '''

    def __init__ (self):

        # Define attributes
        self.tasks_list = []
        self.tasks = []

        # Init credentials
        self.get_credentials(configpath='../config/')

    def get_credentials(self,
                        configpath: str):
        '''Get Google Calendar credentials. The file token.pickle stores
         the user's access and refresh tokens, and is
         created automatically when the authorization flow completes for the first
         time. '''

        creds = None
        token_path = os.path.join(configpath, 'token.pickle')
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                print(f'Reading token {token_path}')
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print("Trying to open credentials.json file")
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('tasks', 'v1', credentials=creds)

    def get_task_list(self):
        ''' Retrieve task list '''
        results = self.service.tasklists().list(maxResults=10).execute()
        items = results.get('items', [])
        self.tasks_list = [x for x in items]


    def get_tasks(self,
                  task_item = 'My Tasks'):
        ''' This function search all tasks into
            specific task listitem '''

        self.get_task_list()
        for item in self.tasks_list:
            if item['title'] == task_item:
                taskID = item['id']
                tasks = self.service.tasks().list(tasklist=taskID).execute()
                for task_item in tasks['items']:    
                    self.tasks.append(task_item['title'])


if __name__ == '__main__':
    tasks = GoogleTasks()

    # Show tasks list
    tasks.get_task_list()
    print('Getting tasklist')
    for task_item in tasks.tasks_list:
        print(task_item['title'])

    # Show tasks into Task Testing task list
    tasks.get_tasks(task_item='Task Testing')
    print('Getting tasks')
    for task_element in tasks.tasks:
        print(task_element)

    

    

    

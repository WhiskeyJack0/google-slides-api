
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

SCOPE = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/presentations', 'https://www.googleapis.com/auth/documents']

class Client:

        def __init__(self):
                #TODO 1: Improve auth flow to not just rely on stored credentials (launching login flow might be too intrusive?)
                #TODO 2: Return proper errors when the google api call fails
                self.creds = ServiceAccountCredentials.from_json_keyfile_name('app/.credentials/service_credentials.json', SCOPE)
                self.slides_service = build('slides', 'v1', credentials=self.creds)
                self.drive_service = build('drive', 'v3', credentials=self.creds)

        def get_slides_service(self):
                return self.slides_service

        def get_presentation(self, presentationID):
                return self.slides_service.presentations().get(presentationId=presentationID).execute()

        def get_slides(self, presentation):
                return presentation.get('slides')
        
        def get_filelist(self):
                results = self.drive_service.files().list(
                pageSize=10, fields="nextPageToken, files(id, name)").execute()
                items = results.get('files', [])
                
                if not items:
                        print('No files found.')
                        return
                return items
        
        def get_file_info(self, fileID):
                results = self.drive_service.revisions().list(fileId=fileID, 
                                        fields='*').execute()
                return results
        
# Main API : returns a dict of slide-ids 
def get_slideid_dict(presentationID):
        client = Client()
        slides = client.get_slides(client.get_presentation(presentationID))
        slide_dict = {}
        for i, slide in enumerate(slides):
                slide_dict[i] = slide.get('objectId')
        slide_dict['total'] = len(slide_dict.keys())
        return slide_dict

#Unused (for now) drive api calls
def get_drive_info():
        client = Client()
        files = client.get_filelist()
        return files
def get_file_info(fileID):
        client = Client()
        files = client.get_file_info(fileID)
        return files

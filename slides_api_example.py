from __future__ import print_function

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google
# If modifying these scopes, delete the file token.json.
# List of permissions that google asks you to authenticate for 
SCOPES = ['https://www.googleapis.com/auth/presentations.readonly', "https://www.googleapis.com/auth/presentations"]

# The ID of a sample presentation.
PRESENTATION_ID = '1IlA5ES-gKdA_ySNXK3SsiQD3D0Oo8NhCSqby7VGrqPQ'


def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def create_slide(presentation_id, page_id, creds):
    """
    Creates the Presentation the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.\n
    """
    # pylint: disable=maybe-no-member
    try:
        service = build('slides', 'v1', credentials=creds)
        # Add a slide at index 1 using the predefined
        # 'TITLE_AND_TWO_COLUMNS' layout and the ID page_id.
        requests = [
            {
                'createSlide': {
                    'objectId': page_id,
                    'insertionIndex': '1',
                    'slideLayoutReference': {
                        'predefinedLayout': 'TITLE_AND_TWO_COLUMNS'
                    }
                }
            }
        ]

        # If you wish to populate the slide with elements,
        # add element create requests here, using the page_id.

        # Execute the request.
        body = {
            'requests': requests
        }
        response = service.presentations() \
            .batchUpdate(presentationId=presentation_id, body=body).execute()
        create_slide_response = response.get('replies')[0].get('createSlide')
        print(f"Created slide with ID:"
              f"{(create_slide_response.get('objectId'))}")
    except HttpError as error:
        print(f"An error occurred: {error}")
        print("Slides not created")
        return error

    return response

def add_image_to_slide(image, creds):
    pass

def list_slides(creds):
    """Shows basic usage of the Slides API.
    Prints the number of slides and elements in a sample presentation.
    """

    try:
        service = build('slides', 'v1', credentials=creds)

        # Call the Slides API
        presentation = service.presentations().get(
            presentationId=PRESENTATION_ID).execute()
       
        slides = presentation.get('slides')

        print('The presentation contains {} slides:'.format(len(slides)))
        for i, slide in enumerate(slides):
            print('- Slide #{} contains {} elements.'.format(
                i + 1, len(slide.get('pageElements'))))
    except HttpError as err:
        print(err)


def main():
    creds = get_credentials();
    #NB: Object id for slide must have length >= 5
    create_slide(PRESENTATION_ID, "sample", creds);


main()

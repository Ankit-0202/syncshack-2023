from __future__ import print_function

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google
from enum import Enum
from dataclasses import dataclass
import json


@dataclass
class Rect():
    x: int
    y: int
    height: int
    width: int


# If modifying these scopes, delete the file token.json.
# List of permissions that google asks you to authenticate for
SCOPES = ['https://www.googleapis.com/auth/presentations.readonly',
          "https://www.googleapis.com/auth/presentations"]

# The ID of a sample presentation.
PRESENTATION_ID = '1IlA5ES-gKdA_ySNXK3SsiQD3D0Oo8NhCSqby7VGrqPQ'


class Layout():
    TITLE_AND_BODY = "TITLE_AND_BODY"
    BLANK = "BLANK"
    TITLE = "TITLE"

# Font size


def getptobj(scalar):
    return {
        'magnitude': scalar,
        'unit': 'PT'
    }


def service_helper(request: dict, creds: str):
    """
        Request object is a dict with keys
        request: function with params "func(service_obj) -> response"
        error_message: string containing error message
        success_message: func with params "success(request response obj) -> None"
    """
    try:
        service = build('slides', 'v1', credentials=creds)

        # Request logic
        func = request["request"]
        error_msg = request["error"]
        success = request["success"]

        response = func(service)
        success(response)
    except HttpError as error:
        print(f"An error occurred: {error}", flush=True)
        print(error_msg, flush=True)
        return error

    return response


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


def create_request_dict(func, success_func, error_msg):
    return {"request": func, "success": success_func, "error": error_msg}


def list_slides(presentation_id, creds):
    """Shows basic usage of the Slides API.
    Prints the number of slides and elements in a sample presentation.
    """
    def func(service):
        presentation = service.presentations().get(
            presentationId=presentation_id).execute()

        slides = presentation.get('slides')
        return slides

    def success(response):
        print('The presentation contains {} slides:'.format(len(response)))
        for i, slide in enumerate(response):
            print('- Slide #{} contains {} elements.'.format(
                i + 1, len(slide.get('pageElements'))))

    error = "failed to list slides"

    request = create_request_dict(func, success, error)
    response = service_helper(request, creds)
    return response


def create_slide(presentation_id, page_id, layout, index, creds):
    """
    Specify index = None to append to end of slide
    Specify page_id = None to generate random page_id

    page_id = None -> {'objectId': 'SLIDES_API1335420809_0'}
    """
    # pylint: disable=maybe-no-member
    def func(service):
        requests = [
            {
                'createSlide': {
                    'objectId': page_id,
                    'insertionIndex': index,
                    'slideLayoutReference': {
                        'predefinedLayout': layout
                    }
                }
            }
        ]

        body = {
            'requests': requests
        }

        response = service.presentations() \
            .batchUpdate(presentationId=presentation_id, body=body).execute()
        create_slide_response = response.get('replies')[0].get('createSlide')
        return create_slide_response

    def success(response):
        print(f"Created slide with ID:"
              f"{(response.get('objectId'))}")

    error = "failed to create slide"

    request = create_request_dict(func, success, error)
    response = service_helper(request, creds)
    return response


def create_textbox_with_text(presentation_id, page_id, textbox_id, rect, text, creds):
    """
    Creates the textbox with text, the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """

    def func(service):
        # Create a new square textbox, using the supplied element ID.

        requests = [
            {
                'createShape': {
                    'objectId': textbox_id,
                    'shapeType': 'TEXT_BOX',
                    'elementProperties': {
                        'pageObjectId': page_id,
                        'size': {
                            'height': getptobj(rect.height),
                            'width': getptobj(rect.width),
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': rect.x,
                            'translateY': rect.y,
                            'unit': 'PT'
                        }
                    }
                }
            },

            # Insert text into the box, using the supplied element ID.
            {
                'insertText': {
                    'objectId': textbox_id,
                    'insertionIndex': 0,
                    'text': text
                }
            }
        ]

        # Execute the request.
        body = {
            'requests': requests
        }

        response = service.presentations() \
            .batchUpdate(presentationId=presentation_id, body=body).execute()
        create_shape_response = response.get('replies')[0].get('createShape')
        return create_shape_response

    def success(response):
        print("Successfully created a text box with response ",
              response)
        return response

    def error():
        print("Failed to create a textbox with given text")

    error = "failed to create slide"

    request = create_request_dict(func, success, error)
    response = service_helper(request, creds)
    return response


def make_textbox_bullets(presentation_id, textbox_id, creds):
    def func(service):
        range = {
            "type": "ALL"
        }

        requests = [{
            "createParagraphBullets": {
                "objectId": textbox_id,
                "textRange": range,
                "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
            }
        }]

        # Execute the request.
        body = {
            'requests': requests
        }

        response = service.presentations() \
            .batchUpdate(presentationId=presentation_id, body=body).execute()
        return response

    def success(response):
        print("Succesfully made textbox bullets")
        return response

    error = "failed to make textbox bullets"

    request = create_request_dict(func, success, error)
    response = service_helper(request, creds)
    return response


def add_image_to_slide(presentation_id, page_id, image_id, img_addr, img_rect, creds):
    def func(service):

        requests = [{
            'createImage': {
                'objectId': image_id,
                'url': img_addr,
                'elementProperties': {
                    'pageObjectId': page_id,
                    'size': {
                        'height': getptobj(img_rect.height),
                        'width': getptobj(img_rect.width)
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': img_rect.x,
                        'translateY': img_rect.y,
                        'unit': 'pt'
                    }
                }
            }
        }]

        body = {
            'requests': requests
        }
        response = service.presentations() \
            .batchUpdate(presentationId=presentation_id, body=body).execute()
        create_image_response = response.get('replies')[0].get('createImage')
        return create_image_response

    def success(response):
        print("successfully added image to slide with response", response)
        return response

    error = "failed to inject image"

    request = create_request_dict(func, success, error)
    response = service_helper(request, creds)
    return response


def add_style(presentationId, objectId, style, textRange, creds):
    def func(service):
        requests = [
            {"updateTextStyle": {
                "objectId": objectId,
                'style': {
                    'bold': True,
                    'italic': True
                },
                "textRange": {
                    "type": "ALL"
                },
                'fields': 'bold,italic',
            }
            }
        ]
        body = {
            "requests": requests
        }

        response = service.presentations() \
            .batchUpdate(presentationId=presentationId, body=body).execute()
        return response

    def success(response):
        print("Successfully styled text")

    error = "Failed to style text"

    request = create_request_dict(func, success, error)
    response = service_helper(request, creds)
    return response


def populate_slides(json_file: str, presentation_id: str):
    creds = get_credentials()

    json_file = open('output.json', 'r')
    json_output = json.load(json_file)
    json_file.close()
    # list_slides(presentation_id, creds)
    if "title" in json_output:
        title = json_output["title"]
        page_id = create_slide(presentation_id, None,
                               Layout.BLANK, None, creds)["objectId"]

        title_rect = Rect(400, 200, 50, 200)
        textbox_id = create_textbox_with_text(
            presentation_id, page_id, page_id+"title", title_rect, title, creds)["objectId"]
        add_style(presentation_id, textbox_id, None, None, creds)

    slide_info = json_output["slides"]
    print(slide_info)

    title_box_rect = Rect(20, 20, 50, 500)
    content_box_rect = Rect(20, 50, 300, 500)
    dim = 512
    scale_factor = 0.3
    new_dim = dim*scale_factor
    image_box_rect = Rect(550, 100, new_dim, new_dim)
    image_counter = 0
    slide_info
    for slide in slide_info:
        page_id = create_slide(presentation_id, None,
                               Layout.BLANK, None, creds)["objectId"]
        print(page_id)
        create_textbox_with_text(
            presentation_id, page_id, page_id+"textbox", title_box_rect, slide["title"], creds)

        dotpoints = "\t" + "\n\t".join(slide["content"])
        create_textbox_with_text(
            presentation_id, page_id, page_id+"bodybox", content_box_rect, dotpoints, creds)
        make_textbox_bullets(presentation_id, page_id+"bodybox", creds)
        if "speaker_notes" in slide:
            add_speaker_notes(presentation_id, page_id,
                              slide["speaker_notes"], creds)

        if len(slide["image_prompts"]) > 0:
            image_url = slide["image_prompts"][0][0]
            add_image_to_slide(presentation_id, page_id, page_id +
                               str(image_counter), image_url, image_box_rect, creds)
            image_counter += 1

    # hardcoded textbox locations: title, content, images


def add_speaker_notes(presentation_id, page_id, speaker_notes, creds):
    def func(service):
        presentation = service.presentations().get(
            presentationId=presentation_id).execute()

        slides = presentation.get('slides')

        def getSlideByObjectId(slides, objectId):
            # Find the slide with the correct page object id
            for slide in slides:
                print(slide["objectId"], objectId)
                if slide["objectId"] == objectId:
                    return slide
            return None

        page = getSlideByObjectId(slides, page_id)
        notesobjid = page["slideProperties"]["notesPage"]["notesProperties"]["speakerNotesObjectId"]

        requests = [{
            "insertText": {
                "objectId": notesobjid,
                "text": speaker_notes,
                "insertionIndex": 0
            }
        }]

        body = {
            'requests': requests
        }

        response = service.presentations() \
            .batchUpdate(presentationId=presentation_id, body=body).execute()
        return response

    def success(response):
        print("succesfully inserted reader notes")

    error = "failed to list slides"

    request = create_request_dict(func, success, error)
    response = service_helper(request, creds)
    return response


def main():
    creds = get_credentials()
    # add_speaker_notes(PRESENTATION_ID, "SLIDES_API1090881242_0", "I love pies", creds)
    populate_slides("output.json", PRESENTATION_ID)
    # # NB: Object id for slide must have length >= 5
    # list_slides(PRESENTATION_ID, creds)

    # new_page = create_slide(PRESENTATION_ID, None,
    #                         Layout.TITLE_AND_BODY, None, creds)
    # page_id = new_page["objectId"]
    # response = create_textbox_with_text(PRESENTATION_ID, page_id,
    #                                     page_id + "textbox", Rect(0, 0, 100, 100), "Ankit is a savage", creds)
    # textbox_id = response["objectId"]
    # make_textbox_bullets(PRESENTATION_ID, textbox_id, creds)
    # add_image_to_slide(PRESENTATION_ID, page_id, None,
    #                    "https://cdn2.stablediffusionapi.com/generations/3c617436-bd0f-4c3c-8782-f0f02c9d1254-0.png", creds)
    # print(response)


if __name__ == "__main__":
    main()

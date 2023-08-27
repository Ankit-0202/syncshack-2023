from flask import Flask, request, session
from my_ai import *
from json import *
from logging import Logger
import sys
from logging.config import dictConfig
from flask_cors import CORS
from slides_api_example import populate_slides, get_slide_pageElement
import json


app = Flask(__name__)
CORS(app)
app.secret_key = "DEV"


@app.post("/prompt-processing")
def process_prompt():

    # Get JSON data sent with POST request
    assert request.json is not None
    json_data = request.json


    # Access prompt data (under "prompt" key)
    prompt_text = json_data["prompt"]
    mood = json_data["mood"]


    # Get object ID
    selected_object_id = json_data["objectID"]
    if selected_object_id is not None:
        session["selected_object_id"] = selected_object_id
    
    elem = get_slide_pageElement(json_data.get("presentationID"), json_data.get("pageID"), json_data.get("objectID"))
    if (elem is not None):
        #otherwise it's just normal page
        #only handle text and image for now
        if (elem.get('shape') is not None): #text
            #generate text
            new_text_out = generate_text(prompt_text, template_partial_txt)
        else: #image
            new_img_out = generate_image(prompt_text, '')
    else:
        generate_json(prompt_text+", and the presentation should have a mood of "+mood);
        json_output = json.load(open("output.json", "r"))
        populate_slides(json_output, '1IlA5ES-gKdA_ySNXK3SsiQD3D0Oo8NhCSqby7VGrqPQ')

    response = {
        "status": "OK",
    }
    return response

@app.before_request
def initialise_session():
    try:
        session["selected_object_id"]
    except KeyError:
        session["selected_object_id"] = None

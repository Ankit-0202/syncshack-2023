from flask import Flask, request, session
from my_ai import *
from json import *


app = Flask(__name__)
app.secret_key = "DEV"


@app.post("/prompt-processing")
def process_prompt():

    # Get JSON data sent with POST request
    assert request.json is not None
    json_data = request.json
    # Access prompt data (under "prompt" key)
    prompt_text = json_data["prompt"]
    # Get object ID
    selected_object_id = json_data["objectID"]
    if selected_object_id is not None:
        session["selected_object_id"] = selected_object_id
    
    print(json_data)
    
    out = generate_text(prompt_text)
    
    print(prompt_text, out, "\n", sep='\n')

    response = {
        "status": "OK",
        "response": out
    }
    
    set_json(out)
    get_images()

    return response


@app.before_request
def initialise_session():
    try:
        session["selected_object_id"]
    except KeyError:
        session["selected_object_id"] = None

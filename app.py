from flask import Flask, request
from my_ai import *
from json import *
from logging import Logger
import sys
from logging.config import dictConfig
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

def call_api(prompt_text):
    # Check if requesting image
    if 'image' in prompt_text:
        return generate_image(prompt_text, "")
    else:
        return generate_text(prompt_text)


@app.post("/prompt-processing")
def process_prompt():

    # Get JSON data sent with POST request
    json_data = request.json
    # Access prompt data (under "prompt" key)
    prompt_text = json_data["prompt"] # type: ignore
    
    out = call_api(prompt_text)

    print(prompt_text, out, "\n", sep='\n', flush=True)
    # print(prompt_text, out, "\n", sep='\n', flush=True, file=sys.stderr)
    # print(prompt_text, out, "\n", sep='\n', flush=True, file=file)
    file = open("output.txt", "w+")

    response = {
        "status": "OK",
        "response": out
    }
    
    set_json(out)
    get_images()

    return response

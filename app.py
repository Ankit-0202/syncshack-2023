from flask import Flask, request
from my_ai import *
from json import *


app = Flask(__name__)

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
    
    print(prompt_text)
    print(out)

    response = {
        "status": "OK",
        "response": out
    }

    return response

from flask import Flask, request
from my_ai import *


app = Flask(__name__)


@app.post("/prompt-processing")
def process_prompt():

    # Get JSON data sent with POST request
    json_data = request.json
    # Access prompt data (under "prompt" key)
    prompt_text = json_data["prompt"] # type: ignore
    
    out = ""
    
    # Check if requesting image
    if 'image' in prompt_text:
        out = generate_image(prompt_text, "")
    
    else:
        out = generate_text(prompt_text)
    
    print(prompt_text)
    print(out)

    response = {
        "status": "OK",
        "response": out
    }

    return response

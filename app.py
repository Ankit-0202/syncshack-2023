from flask import Flask, request
from my_ai import *


app = Flask(__name__)


@app.post("/prompt-processing")
def process_prompt():
    # TODO: Backend prompt processing

    # Get JSON data sent with POST request
    json_data = request.json
    # Access prompt data (under "prompt" key)
    prompt_text = json_data["prompt"] # type: ignore
    
    print(prompt_text)
    
    
    out = ""
    
    # Check if requesting image
    if 'image' in prompt_text:
        out = generate_image(prompt_text, "")
    
    else:
        out = generate_text(prompt_text)
    
    
    
    
    
    
    

    response = {
        "status": "OK",
    }

    return response

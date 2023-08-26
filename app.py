from flask import Flask, request
from my_ai import *
from json import *


app = Flask(__name__)


@app.post("/prompt-processing")
def process_prompt():

    # Get JSON data sent with POST request
    json_data = request.json
    # Access prompt data (under "prompt" key)
    prompt_text = json_data["prompt"] # type: ignore
    
    out = generate_text(prompt_text)
    
    print(prompt_text, out, "\n", sep='\n')

    response = {
        "status": "OK",
        "response": out
    }
    
    set_json(out)
    get_images()

    return response
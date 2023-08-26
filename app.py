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
    
    print(prompt_text, out, sep='\n')

    response = {
        "status": "OK",
        "response": out
    }
    
    set_json(out)
    get_images()

    return response


def set_json(output):
    with open('output.json', 'w+') as json_file:
        json_file.write(output)
        

def get_images():
    json_file = open('output.json', 'r')
    json_output = json.load(json_file)
    json_file.close()
        
    # Loop through each slide and modify image prompts
    for slide_index, slide in enumerate(json_output['slides']):
        image_prompts = slide["image_prompts"]
        
        for image_index, prompt in enumerate(image_prompts):
            json_output[slide][image_index] = generate_image(prompt, "")
            

    # Save the modified data back to the JSON file
    with open('output.json', 'w') as json_file:
        json.dump(json_output, json_file, indent=2)
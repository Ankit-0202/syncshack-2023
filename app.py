from flask import Flask, request


app = Flask(__name__)


@app.post("/prompt-processing")
def process_prompt():
    # TODO: Backend prompt processing

    # Get JSON data sent with POST request
    json_data = request.json
    # Access prompt data (under "prompt" key)
    prompt_text = json_data["prompt"] # type: ignore

    response = {
        "status": "OK"
    }

    return response

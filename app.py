from flask import Flask


app = Flask(__name__)


@app.post("/prompt-processing")
def process_prompt():
    # TODO: Backend prompt processing
    response = {
        "status": "OK"
    }

    return response

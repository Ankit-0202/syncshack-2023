import os
import openai
import json
import requests 

#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SD_API_KEY = os.getenv("SD_API_KEY")

openai.api_key = os.getenv("OPENAI_API_KEY")
print(openai.api_key);

def openai_prompt(my_prompt: str):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=my_prompt,
        max_tokens=10
    )
    return response.choices[0].text.strip()

def generate_image(my_prompt: str, neg_prompt:str):
    url = "https://stablediffusionapi.com/api/v3/text2img"

    payload = json.dumps({
        "key": SD_API_KEY,
        "prompt": my_prompt,
        "negative_prompt": None if len(neg_prompt) == 0 else None,
        "width": "512",
        "height": "512",
        "samples": "1",
        "num_inference_steps": "20",
        "seed": None,
        "guidance_scale": 7.5,
        "safety_checker": "yes",
        "multi_lingual": "no",
        "panorama": "no",
        "self_attention": "no",
        "upscale": "no",
        "webhook": None,
        "track_id": None
    })

    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print("Please find your image at", response.json())


if __name__ == "__main__":
    option = input("Choose an option (A) generate text (B) generate image: ")
    option = option.upper()
    if option != "A" and option != "B":
        print("Invalid option");
        exit();
    
    prompt = input("Please enter a prompt: ")
    if (option == "B"):
        neg_prompt = input("Please enter a negative prompt (leave empty for nothing): ")
        generate_image(prompt, neg_prompt)
    elif (option == "A"):
        print(openai_prompt(prompt))

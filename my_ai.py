import os
import os.path
import openai
import json
import requests 

import mood_langchain


############################
######### API KEYS #########
############################
SD_API_KEY = os.getenv("SD_API_KEY")
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")


############################
######### TEMPLATE #########
############################
template_file = open("template.txt", "r")
template_txt = template_file.read()
template_file.close()




def generate_text(my_prompt: str, template = template_txt):
    # template = """You are an assistant who generates words depending on the user's adjective and mood.
    #     A user will pass in two words. The first word will contain the adjective and the second word will contain the mood;
    #     you should generate 5 synonyms of that adjective that fits the mood in a comma separated list.
    #     ONLY return a comma separated list, and nothing more."""
    # print("Input two words, adjective and mood modifier")
    
    return mood_langchain.langchainApply(template, my_prompt)


def generate_image(my_prompt: str, neg_prompt: str):
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
    return response.json()['output']


def set_json(output):
    with open('output.json', 'w+') as json_file:
        json_file.write(output)
        

def get_images():
    json_file = open('output.json', 'r')
    json_output = json.load(json_file)
    json_file.close()
        
    # Loop through each slide and modify image prompts
    # Iterate through each slide
    for i, slide in enumerate(json_output['slides']):
        print(f"Slide {i + 1}: {slide['title']}")
        
        # Iterate through each image_prompt item
        ip = 'image_prompts'
        if ip in slide:
            for j, item in enumerate(slide[ip]):
                slide[ip][j] = generate_image(slide[ip][j], "")
                print(f"{j}: {slide[ip][j]}")
            
                print("--------")
        print("\n----------------\n")
            

    # Save the modified data back to the JSON file
    with open('output.json', 'w') as json_file:
        json.dump(json_output, json_file, indent=2)










if __name__ == "__main__":
    option = input("Choose an option (A) generate text (B) generate image: ")
    option = option.upper()
    if option != "A" and option != "B":
        print("Invalid option")
        exit()
    
    prompt = input("Please enter a prompt: ")
    
    if (option == "A"):
        out = generate_text(prompt)
        print(out)
        set_json(out)
        get_images()
        
    elif (option == "B"):
        neg_prompt = input("Please enter a negative prompt (leave empty for nothing): ")
        print(generate_image(prompt, neg_prompt))

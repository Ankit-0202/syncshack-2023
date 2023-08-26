import os
import os.path
import openai
import json
import requests 

import mood_langchain
import bcrypt
from cryptography.fernet import Fernet


############################
######### API KEYS #########
############################
SD_API_KEY = os.getenv("SD_API_KEY")
# SD_API_KEY = ''
openai.api_key = os.getenv("OPENAI_API_KEY")

# pwd_hash = b'$2b$12$FBKIC4h4fy2Bo9XhCgCzlehrYCpWaZEwgegzDdqm3OilytsMg.hRC'
# key_crypt = b'q3UGH3GalYYT6CqH_7b2KsSdZEUf5e-6ZwQxtJVPwSU='
# token_crypt = b'gAAAAABk6m_uQltJ7TnjN0RrSc0b0Q41gxnoz6PkYM8yFs_nA1FsxrAKI2vD-p7qQFQ0VnikFKveUBSvnSIaXycTlQPrhYIgAWCi-vGozCBm8FY9HliNvnM0ltNLnfjM9TOEVGT6O86IkXWCMD593_z09rj-ezaZ_w=='
# sd_token_crypt = b'gAAAAABk6nGfbZ_LgJMgBNUTacz2XnBjCiOwdCB6eM9UxDOWgHIZcCw2Qm6ug32NJJRF6jHMZGk0X4oFZF1ArLCPbu3f5-oXzre5YKR60D_vBOd_ctaB9qyhof1KEEI_iOduogCyVLgvNSlCy3RMtyC18IajHXeePw=='

# pwd = input('enter password: ')
# if bcrypt.checkpw(pwd.encode('utf-8'), pwd_hash):
#     f = Fernet(key_crypt)
#     openai.api_key = f.decrypt(token_crypt)
#     SD_API_KEY = f.decrypt(sd_token_crypt)
# else:
#     raise ValueError("Bad password")
# pwd = ''

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
    try:
        if response.json()['output']:
            return response.json()['output']
    except:
        pass


def set_json(output):
    with open('output.json', 'w+') as json_file:
        json_file.write(output)
        

def get_images():
    json_file = open('output.json', 'r')
    json_output = json.load(json_file)
    json_file.close()
        
    # Loop through each slide and modify image prompts
    # Iterate through each slide
    
    print("---GENERATING IMAGES---")
    for i, slide in enumerate(json_output['slides']):
        print(f"Slide {i + 1}: {slide['content']}\n")
        
        # Iterate through each image_prompt item
        ip = 'image_prompts'
        if ip in slide:
            num_images = 0
            for j, item in enumerate(slide[ip]):
                image = generate_image(slide[ip][j], "text")
                if image is not None:
                    slide[ip][j] = image
                    num_images += 1
                    print(f"Image {num_images}: {slide[ip][j]}")
                    print("--------")
                    
        print("\n---------------------\n")
            

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

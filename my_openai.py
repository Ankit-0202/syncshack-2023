import os
import openai

openai.api_key = os.getenv("OPENAI_KEY")

def openai_prompt(my_prompt: str):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=my_prompt,
        max_tokens=10
    )
    return response.choices[0].text.strip()



if __name__ == "__main__":
    prompt = input()
    print(openai_prompt(prompt))

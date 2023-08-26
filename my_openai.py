import os
import openai

openai.api_key = "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"

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
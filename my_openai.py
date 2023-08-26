import os
import openai

openai.organization = "YOUR_ORG_ID"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()

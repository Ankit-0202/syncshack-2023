#pip install langchain openai
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser

class RawOutputParser(BaseOutputParser):
    def parse(self, text:str):
        return text

chat = ChatOpenAI()

def langchainApply(template: str, humanPrompt: str):
    
    # template = """You are an assistant who generates words depending on the user's adjective and mood.
    # A user will pass in two words. The first word will contain the adjective and the second word will contain the mood;
    # you should generate 5 synonyms of that adjective that fits the mood in a comma separated list.
    # ONLY return a comma separated list, and nothing more."""

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    chain = LLMChain(
        llm=chat,
        prompt=chat_prompt,
        output_parser=RawOutputParser()
    )
    return chain.run(humanPrompt)

if __name__ == "__main__":
    template = """You are an assistant who generates words depending on the user's adjective and mood.
    A user will pass in two words. The first word will contain the adjective and the second word will contain the mood;
    you should generate 5 synonyms of that adjective that fits the mood in a comma separated list.
    ONLY return a comma separated list, and nothing more."""
    print(langchainApply(template, "love angry"))
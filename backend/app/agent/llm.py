from config import env

from langchain_openai import ChatOpenAI
from langchain_litellm import ChatLiteLLM

if env.OPENAI_API_KEY:
    llm = ChatOpenAI(api_key=env.OPENAI_API_KEY, model="gpt-4.1") #type: ignore
elif env.LITELLM_API_KEY:
    llm = ChatLiteLLM(api_key=env.LITELLM_API_KEY, api_base="https://llm.keyvalue.systems", model="litellm_proxy/gpt-4.1")

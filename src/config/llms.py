import logging
import os

from dotenv import dotenv_values, load_dotenv
from langchain_openai import AzureChatOpenAI

# Load variables from .env file into a dictionary
if os.path.exists(".env"):
    load_dotenv()
    config_env = dotenv_values(".env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
base_model = AzureChatOpenAI(
    api_key=config_env.get("AZURE-OPENAI-API-KEY-GPT4"),
    azure_endpoint=config_env.get("AZURE-OPENAI-ENDPOINT-GPT4"),
    api_version=config_env.get("OPENAI-API-VERSION-GPT4"),
    azure_deployment=config_env.get("AZURE-DEPLOYMENT-GPT4"),
    model_name=config_env.get("AZURE-OPENAI-GPT4-MODEL-NAME", "gpt-4"),
    temperature=0,
)

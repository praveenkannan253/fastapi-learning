from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name:str = "Groq Chatbot App"
    groq_api_key:str
    model:str = "openai/gpt-oss-120b"

    class Config:
        env_file=".env"

settings=Settings()
from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    groq_api_key:str
    database_url:str
    debug:bool=False

    class Config:
        env_file=".env"

settings=Setting()
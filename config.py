from pydantic import BaseSettings



class Settings(BaseSettings):
    algorithm : str
    access_token_expire_time : int
    encryption_key: str 
    secret_key : str
    

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()

print(get_settings().algorithm)

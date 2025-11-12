from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Use a single, consistent name for the API key used by LangChain
    api_key: str 
    backend_api_key: str = 'super-secret-extension-key'
    host: str = '0.0.0.0'
    port: int = 8000
    vector_dir: str = './db'
    embed_model: str = 'text-embedding-3-small'
    llm_model: str = 'meta-llama/llama-3.3-8b-instruct:free'
    

    # Pydantic V2 style for configuration
    model_config = SettingsConfigDict(env_file='./backend/.env')

settings = Settings()
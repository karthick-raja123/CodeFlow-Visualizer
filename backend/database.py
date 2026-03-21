from pydantic_settings import BaseSettings
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    mongodb_url: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    db_name: str = os.getenv("DB_NAME", "codevisualizer")

settings = Settings()

client = AsyncIOMotorClient(settings.mongodb_url)
db = client[settings.db_name]
sessions_collection = db["sessions"]

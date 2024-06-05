# app/db.py

from pymongo import MongoClient
from pymongo.errors import ConfigurationError
from .config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db():
    try:
        client = MongoClient(Config.MONGO_URI)
        # Verify the connection by listing the databases
        client.list_database_names()
        db = client[Config.DATABASE_NAME]
        logger.info("Connected to MongoDB successfully.")
        return db
    except ConfigurationError as e:
        logger.error(f"Connection to MongoDB failed: {e}")
        return None

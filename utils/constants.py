from dataclasses import dataclass
from os import getenv


@dataclass
class Constants:
    DB_PATH = getenv("DB_PATH", "/data")
    COLLECTION = getenv("COLLECTION", "test_collection")

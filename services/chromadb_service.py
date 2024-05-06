import os
from utils.logger import logger
from utils.constants import Constants

from chromadb import PersistentClient


class ChromaDBService:
    def __init__(self):
        data_persistent_dir = os.path.join(os.getcwd(), "models")
        self._client = PersistentClient(path=data_persistent_dir)

        try:
            self._collection = self._client.get_collection(Constants.COLLECTION)
        except Exception as e:
            logger.error(e)
            self._collection = self._client.create_collection(
                name=Constants.COLLECTION,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("test_collection created")
        finally:
            logger.info("ChromaDB server is ready")

    def add_embedding(self, document, embedding, id_):
        self._collection.add(
            documents=[document],
            embeddings=[embedding],
            ids=[id_]
        )

    def query(self, embedding):
        resp = self._collection.query(
            n_results=10,
            query_embeddings=[embedding]
        )

        return resp

    def delete_by_id(self, id_):
        self._collection.delete(
            ids=[id_]
        )

    def reset_db(self):
        self._client.delete_collection(Constants.COLLECTION)
        self._collection = self._client.create_collection(
                name=Constants.COLLECTION,
                metadata={"hnsw:space": "cosine"}
            )

import json
from utils.logger import logger

from flask import Flask, Response, request
from flask_cors import CORS

import numpy as np

from services.chromadb_service import ChromaDBService

app = Flask(__name__)
CORS(app)

chroma_client = ChromaDBService()


@app.get("/health_check")
def health_check():
    return Response(
        status=200,
        response=json.dumps({
            "status": "ok"
        })
    )


@app.post("/add_embedding")
def add_embedding():
    try:
        req_body_json = request.get_json()
        logger.info(f"Document : {req_body_json.get('documents')}")
        logger.info(f"ID : {req_body_json.get('id')}")

        embeddings = req_body_json.get("embeddings")
        embedding = np.array(embeddings["embedding"]).tolist()

        chroma_client.add_embedding(
            document=req_body_json.get("documents"),
            embedding=embedding[0][0],
            id_=req_body_json.get("id")
        )

        return Response(
            status=200,
            response=json.dumps({
                "status": "added embedding successfully"
            })
        )
    except Exception as err:
        logger.error(f"Error in adding embedding : {err}")
        return Response(
            status=500,
            response=json.dumps({
                "status": "Failed to add embedding",
                "error": str(err)
            })
        )


@app.post("/get_similar_image")
def get_similar_image():
    try:
        req_body_json = request.get_json()
        embedding_to_search = req_body_json.get("embedding")
        embedding = np.array(embedding_to_search).tolist()

        resp = chroma_client.query(
            embedding=embedding[0][0],
        )

        return Response(
            status=200,
            response=json.dumps({
                "status": resp
            })
        )
    except Exception as err:
        logger.error(f"Error in fetching similar images : {err}")
        return Response(
            status=500,
            response=json.dumps({
                "status": "Error in fetching similar images",
                "error": str(err)
            })
        )


@app.delete("/delete_id_from_coll/<id>")
def delete_id_from_coll(id_):
    try:
        chroma_client.delete_by_id(
            id_=id_
        )

        return Response(
            status=200,
            response=json.dumps({
                "status": "Delete ID successfully"
            })
        )
    except Exception as err:
        logger.error(f"Error in Deleting ID : {err}")
        return Response(
            status=500,
            response=json.dumps({
                "status": "Error in Deleting ID",
                "error": str(err)
            })
        )


@app.get("/reset_db")
def reset_db():
    try:
        chroma_client.reset_db()
        return Response(
            status=200,
            response=json.dumps({
                "status": "Success"
            })
        )
    except Exception as err:
        logger.error(f"Error in resetting DB : {err}")
        return Response(
            status=500,
            response=json.dumps({
                "status": "Failed",
                "error": str(err)
            })
        )


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5646)

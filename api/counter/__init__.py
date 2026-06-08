import azure.functions as func
import json
import os
from azure.cosmos import CosmosClient, exceptions

def main(req: func.HttpRequest) -> func.HttpResponse:
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json"
    }

    if req.method == "OPTIONS":
        return func.HttpResponse(status_code=204, headers=headers)

    try:
        endpoint = os.environ["COSMOS_ENDPOINT"]
        key      = os.environ["COSMOS_KEY"]

        client    = CosmosClient(endpoint, key)
        db        = client.get_database_client("ResumeDB")
        container = db.get_container_client("counter")

        try:
            item = container.read_item(item="counter", partition_key="counter")
            item["count"] += 1
        except exceptions.CosmosResourceNotFoundError:
            item = {"id": "counter", "count": 1}

        container.upsert_item(item)

        return func.HttpResponse(
            json.dumps({"count": item["count"]}),
            status_code=200,
            headers=headers
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps({"count": 0, "error": str(e)}),
            status_code=500,
            headers=headers
        )
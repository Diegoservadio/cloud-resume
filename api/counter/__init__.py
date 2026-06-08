import azure.functions as func
import json
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json"
    }

    endpoint = os.environ.get("COSMOS_ENDPOINT", "MANCANTE")
    key = os.environ.get("COSMOS_KEY", "MANCANTE")

    # Debug temporaneo: restituisce le variabili (prime 10 lettere)
    return func.HttpResponse(
        json.dumps({
            "endpoint_preview": endpoint[:30],
            "key_found": len(key) > 10
        }),
        status_code=200,
        headers=headers
    )
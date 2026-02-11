import azure.functions as func
import logging
import io
import json
import os

from azure.storage.blob import BlobServiceClient
import pandas as pd

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        result = process_nutritional_data_from_azurite()
        return func.HttpResponse(result)
    except Exception as exc:
        logging.exception("Failed to process nutritional data.")
        return func.HttpResponse(
            f"Processing failed: {exc}",
            status_code=500,
        )

def process_nutritional_data_from_azurite():
    connect_str = os.getenv("AzureWebJobsStorage")
    if not connect_str:
        raise ValueError("AzureWebJobsStorage is not set.")

    # Pin to an Azurite-supported API version.
    blob_service_client = BlobServiceClient.from_connection_string(
        connect_str,
        api_version="2021-12-02",
    )

    container_name = 'datasets'
    blob_name = 'All_Diets.csv'

    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)

    if not blob_client.exists():
        return (
            f"Blob '{blob_name}' not found in container '{container_name}'. "
            "Upload it to Azurite and retry."
        )

    # Download blob content to bytes
    stream = blob_client.download_blob().readall()
    df = pd.read_csv(io.BytesIO(stream))

    # Calculate averages
    avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()

    # Save results locally as JSON (simulate NoSQL storage)
    result = avg_macros.reset_index().to_dict(orient='records')
    os.makedirs('simulated_nosql', exist_ok=True)
    with open('simulated_nosql/results.json', 'w') as f:
        json.dump(result, f)

    return "Data processed and stored successfully."

if __name__ == "__main__":
    print(process_nutritional_data_from_azurite())


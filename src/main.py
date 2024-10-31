import logging

from fastapi import FastAPI, HTTPException
from .models import APIModel, RequestData
from .validators import validate_parameters
from typing import Dict, List

app = FastAPI()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

models_db: Dict[str, APIModel] = {} # in memory storage for models

@app.post("/models")
def add_model(models: List[APIModel]):
    """
    Adds a list of API models to the models database. Each model is stored
    with a unique key based on its path and method.

    Parameters:
        models (List[APIModel]): List of API models with path, method, and validation parameters.

    Returns:
        dict: Confirmation message after adding models to the database.
    """
    for model in models:
        model_key = f"{model.path}_{model.method}"

        exist_model = models_db.get(model_key)
        if exist_model:
            logger.info(f"{model_key} API model already exist...")
            continue

        logger.info(f"Add {model_key} API model")
        models_db[model_key] = model

    return {"message": "Models added successfully"}

@app.post("/validate")
def validate_request(request_data: RequestData):
    """
    Validates an incoming request by comparing its parameters (query params, headers, body)
    against a stored model to identify any abnormalities.

    Parameters:
        request_data (RequestData): Incoming request details, including path, method, query params, headers, and body.

    Returns:
        dict: JSON indicating if the request is abnormal. If so, it includes details of the abnormal fields.
    """
    key = f"{request_data.path}_{request_data.method}"
    model = models_db.get(key)
    
    if not model:
        raise HTTPException(status_code=404, detail="Model not found for the given path and method")
    
    logger.info(f"Starting validation for request model - method: {request_data.method}, path: {request_data.path}")
    
    anomalies = {
        "query_params": validate_parameters(request_data.query_params, model.query_params),
        "headers": validate_parameters(request_data.headers, model.headers),
        "body": validate_parameters(request_data.body, model.body)
    }
    
    abnormal_fields = {k: v for k, v in anomalies.items() if v}
    
    if abnormal_fields:
        return {"is_abnormal": True, "abnormal_fields": abnormal_fields}
    else:
        return {"is_abnormal": False, "message": "Request is valid"}
import re
import datetime

from typing import List, Dict, Any

def validate_type(value: Any, expected_types: List[str]) -> bool:
    """
    Validates if a given value matches one of the expected types.

    Args:
        value (Any): The value to be validated.
        expected_types (List[str]): A list of expected type names ("Int", "String", etc.).

    Returns:
        bool: True if the value matches one of the expected types, False otherwise.
    """
    for expected_type in expected_types:
        if expected_type == "Int" and isinstance(value, int):
            return True
        elif expected_type == "String" and isinstance(value, str):
            return True
        elif expected_type == "Boolean" and isinstance(value, bool):
            return True
        elif expected_type == "List" and isinstance(value, list):
            return True
        elif expected_type == "Date" and isinstance(value, str):
            try:
                datetime.datetime.strptime(value, "%d-%m-%Y")
                return True
            except ValueError:
                continue
        elif expected_type == "Email" and isinstance(value, str):
            if re.match(r"[^@]+@[^@]+\.[^@]+", value):
                return True
        elif expected_type == "UUID" and isinstance(value, str):
            if re.match(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$", value):
                return True
        elif expected_type == "Auth-Token" and isinstance(value, str):
            if value.startswith("Bearer ") and re.match(r"Bearer [a-zA-Z0-9]+", value):
                return True
    return False

def validate_parameters(request_params: List[Dict[str, Any]], model_params: List[Any]) -> List[Dict[str, str]]:
    """
    Validates the parameters of a request against a defined model.

    Args:
        request_params (List[Dict[str, Any]]): A list of request parameters, each containing a name and value.
        model_params (List[Any]): A list of model parameters that define the expected structure and types.

    Returns:
        List[Dict[str, str]]: A list of errors found during validation, each containing the parameter name and reason for the error.
    """
    errors = []
    model_params_dict = {p.name: p for p in model_params}
    
    for param in request_params:
        model_param = model_params_dict.get(param.name)

        if not model_param:
            errors.append({"name": param.name, "reason": "Unexpected parameter"})
            continue
        if not validate_type(param.value, model_param.types):
            errors.append({"name": param.name, "reason": f"Type mismatch. Expected types: {model_param.types}"})
    
    # check for missing required parameters
    for model_param in model_params:
        is_missing_required = model_param.required and model_param.name not in [p.name for p in request_params]
        
        if is_missing_required:
            errors.append({"name": model_param.name, "reason": "Missing required parameter"})
    
    return errors

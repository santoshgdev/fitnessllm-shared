"""Cloud utils."""
import json
from os import environ

from beartype import beartype
from google.cloud import secretmanager

from fitnessllm_shared.logger_utils import structured_logger


@beartype
def get_secret(name: str) -> dict:
    """Retrieve secret from secret manager."""
    if "PROJECT_ID" not in environ:
        raise KeyError("PROJECT_ID environment variable not found")
    structured_logger.info(message="Initializing secret manager", service="shared")
    client = secretmanager.SecretManagerServiceClient()
    structured_logger.info(message=f"Getting secret for {name}", service="shared")
    try:
        response = client.access_secret_version(
            request={
                "name": f"projects/{environ['PROJECT_ID']}/secrets/{name}/versions/latest",
            }
        )
        structured_logger.info(message=f"Retrieved secret {name}", service="shared")
        secret_payload = response.payload.data.decode("UTF-8")
        try:
            return json.loads(secret_payload)
        except json.JSONDecodeError:
            return secret_payload
    except Exception as e:
        structured_logger.error(
            message=f"Failed to retrieve or decode secret {name}: {e}", service="shared"
        )
        raise

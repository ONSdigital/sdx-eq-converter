import structlog

from app import CONFIG


logger = structlog.get_logger()


def write_to_bucket(data: bytes, filename: str):
    """
    Uploads a string submission to the correct folder within the GCP outputs bucket.
    """
    logger.info("Uploading to bucket")
    logger.info(f"Storing as {filename}")
    blob = CONFIG.BUCKET.blob(filename)
    blob.upload_from_string(data)
    logger.info(f"Successfully uploaded: {filename}")

import structlog

from app import CONFIG


logger = structlog.get_logger()


def write_to_bucket(data: str, filename: str) -> str:
    """
    Uploads a string submission to the correct folder within the GCP outputs bucket.
    """
    logger.info("Uploading to bucket")
    # remove destination suffix
    name = filename.split(":")[0]
    path = f"{name}"
    logger.info(f"Storing as {path}")
    blob = CONFIG.BUCKET.blob(path)
    blob.upload_from_string(data)
    logger.info(f"Successfully uploaded: {filename}")
    return path

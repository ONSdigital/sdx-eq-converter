import structlog

from app.store import write_to_bucket

logger = structlog.get_logger()


def process(tx_id: str, data_bytes: bytes):

    logger.info("Storing to bucket")
    write_to_bucket(data=data_bytes, filename=tx_id)

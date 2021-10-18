import hashlib

import structlog

from app.store import write_to_bucket

logger = structlog.get_logger()


def process(tx_id : str, data_bytes: bytes):

    logger.info("Storing to bucket")
    path = write_to_bucket(filename=tx_id)

    logger.info("Sending DAP notification")


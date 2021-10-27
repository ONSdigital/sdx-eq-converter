from app import CONFIG


def quarantine_submission(data_str: str, tx_id: str, error: str):
    """Publish the submission represented by data_str to the quarantine topic"""

    data = data_str.encode("utf-8")
    future = CONFIG.QUARANTINE_PUBLISHER.publish(CONFIG.QUARANTINE_TOPIC_PATH, data, tx_id=tx_id, error=error)
    return future.result()

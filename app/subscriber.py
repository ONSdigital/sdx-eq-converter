import threading

import structlog
from structlog.contextvars import bind_contextvars

from app import CONFIG

logger = structlog.get_logger()


def callback(message):
    tx_id = message.attributes.get('tx_id')
    bind_contextvars(app="SDX-EQ-Converter")
    bind_contextvars(tx_id=tx_id)
    bind_contextvars(thread=threading.currentThread().getName())
    logger.info(f"tx_id = {tx_id}")
    message.ack()


def start():
    """
    Begin listening to the survey pubsub subscription.

    This functions spawns new threads that listen to the subscription topic and
    on receipt of a message invoke the callback function

    The main thread blocks indefinitely unless the connection times out

    """

    streaming_pull_future = CONFIG.SURVEY_SUBSCRIBER.subscribe(CONFIG.SURVEY_SUBSCRIPTION_PATH, callback=callback)
    logger.info(f"Listening for messages on {CONFIG.SURVEY_SUBSCRIPTION_PATH}..\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with CONFIG.SURVEY_SUBSCRIBER:
        try:
            # Result() will block indefinitely, unless an exception is encountered first.
            streaming_pull_future.result()
        except TimeoutError as te:
            logger.error("TimeoutError error, stopping listening", error=str(te))
            streaming_pull_future.cancel()

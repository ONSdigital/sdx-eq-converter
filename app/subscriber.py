import threading

import structlog
from structlog.contextvars import bind_contextvars, clear_contextvars

from app import CONFIG
from app.eq_converter import process
from app.quarantine import quarantine_submission

logger = structlog.get_logger()


def callback(message):
    tx_id = message.attributes.get('tx_id')
    bind_contextvars(app="SDX-EQ-Converter")
    bind_contextvars(tx_id=tx_id)
    bind_contextvars(thread=threading.currentThread().getName())
    encrypted_response_str = None

    try:
        encrypted_response_str = message.data.decode('utf-8')
        process(tx_id, encrypted_response_str)

    except Exception as error:
        if encrypted_response_str is None:
            logger.error("encrypted_response_str is none, quarantining response instead!")
            quarantine_submission("no data", tx_id, str(error))
        else:
            logger.error(f"quarantining response: {error}")
            quarantine_submission(encrypted_response_str, tx_id, str(error))

    finally:
        clear_contextvars()
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

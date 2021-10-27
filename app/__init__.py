import os
from google.cloud import pubsub_v1, storage
from app.logger import logging_config

logging_config()

project_id = os.getenv('PROJECT_ID', 'ons-sdx-sandbox')
subscription_id = "survey-subscription"
quarantine_topic_id = "quarantine-survey-topic"


class Config:
    """Class to hold required configuration data"""

    def __init__(self, proj_id) -> None:
        self.PROJECT_ID = proj_id
        self.SURVEY_SUBSCRIBER = None
        self.SURVEY_SUBSCRIPTION_PATH = None
        self.QUARANTINE_PUBLISHER = None
        self.QUARANTINE_TOPIC_PATH = None
        self.BUCKET_NAME = f'{proj_id}-survey-responses'
        self.BUCKET = None


CONFIG = Config(project_id)


def cloud_config():
    """
    Loads configuration required for running against GCP based environments

    This function makes calls to GCP native tools such as Google Secret Manager
    and therefore should not be called in situations where these connections are
    not possible, e.g running the unit tests locally.
    """

    survey_subscriber = pubsub_v1.SubscriberClient()
    CONFIG.SURVEY_SUBSCRIPTION_PATH = survey_subscriber.subscription_path(project_id, subscription_id)
    CONFIG.SURVEY_SUBSCRIBER = survey_subscriber

    quarantine_publisher = pubsub_v1.PublisherClient()
    CONFIG.QUARANTINE_TOPIC_PATH = quarantine_publisher.topic_path(project_id, quarantine_topic_id)
    CONFIG.QUARANTINE_PUBLISHER = quarantine_publisher

    storage_client = storage.Client(CONFIG.PROJECT_ID)
    CONFIG.BUCKET = storage_client.bucket(CONFIG.BUCKET_NAME)

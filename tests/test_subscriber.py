import unittest
from unittest import mock
from unittest.mock import patch, Mock

from google.cloud.pubsub_v1.subscriber.message import Message
from app.subscriber import callback


class TestSubsrciber(unittest.TestCase):

    @patch.object(Message, 'ack')
    @mock.patch('app.subscriber.process')
    @mock.patch('app.subscriber.quarantine_submission')
    def test_quarantine_with_data(self, quarantine_submission, mock_process, mock_message):
        mock_message.data = b'Test Data'
        mock_process.side_effect = Exception
        callback(mock_message)
        quarantine_submission.assert_called()

    @mock.patch('app.subscriber.process')
    def test_callback(self, mock_process):
        tx_id = "123"
        mock_message = Mock()
        mock_message.attributes.get.return_value = tx_id
        mock_message.data.decode.return_value = 'my message'
        callback(mock_message)
        mock_message.ack.assert_called()

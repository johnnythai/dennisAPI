from django.test import TestCase
from channels.testing import HttpCommunicator
from .consumers import TestConsumer
from channels.testing import WebsocketCommunicator
import json

class MyTests(TestCase):
    async def test_ws_consumer(self):
        communicator = WebsocketCommunicator(TestConsumer.as_asgi(), "/testws/")
        connected = await communicator.connect()
        assert connected
        print('test case connected to consumer')

        # Test sending text
        await communicator.send_to(text_data='> consumer: This message is for the consumer')
        response = await communicator.receive_from()
        print('< consumer: ', response)
        assert response

        # Close
        await communicator.disconnect()
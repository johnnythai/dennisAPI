import json    
from asgiref.sync import async_to_sync
from .tasks import websocket_client
from channels.generic.websocket import WebsocketConsumer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import AnonymousUser, User


class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, code):
        self.close()

    def receive(self, text_data):
        print(text_data)
        self.send(text_data="Test success!")

class AlpacaConsumer(WebsocketConsumer):
    """
    Connects to alpaca.markets websocket. Connected clients can subscribe and listen to channels.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # alpaca data stored on consumer instance
    channels = []
    data = {}

    def connect(self):
        """
        Authorize user before accepting connection.
        """
        user = self.scope['user']
        print(type(user))

        if isinstance(user, AnonymousUser):
            print('not auth')
            self.group_name = 'group1'
            # join group
            async_to_sync(self.channel_layer.group_add)(
                self.group_name,
                self.channel_name
            )
            self.accept()
            self.close()

        elif isinstance(user, User):
            self.group_name = 'group1'
            # join group
            async_to_sync(self.channel_layer.group_add)(
                self.group_name,
                self.channel_name
            )
            self.accept()

            print('Connected to AlpacaConsumer', self)
            print('CHANNEL NAME: ', self.channel_name)
            print('CHANNEL LAYER: ', self.channel_layer)
            print('CHANNEL GROUP: ', self.group_name)
        
    def disconnect(self):
        print('closing connection...')
        # self.websocket.close()
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def consumer_message(self, event):
        """
        Receive channel state from websocket and send to client.
        message = {'message':{'Subscriptions': channels}}
        """
        message = event['message']
        channels = message['message']['subscriptions']
        print('< (websocket): current subscriptions ', channels)
        for channel in channels:
            if channel not in self.channels:
                self.channels.append(channel)

        self.send(json.dumps({
            'message': {'subscriptions': self.channels}
        }))

    def client_message(self, event):
        """
        Send websocket data to client. From Consumer group.
        """
        message = event['message']
        print('> (client): ', message)

        self.send(json.dumps(message))

    def connect_websocket(self, ws_message):
        """
        Connect to alpaca websocket if self.channels.
        Run lister function as backgroung task.

        :param ws_message: message from receive() method.
        :type ws_message: str
        """

        print('Connecting to websocket...')
        websocket_client.delay(self.group_name, ws_message)
        
    def receive(self, text_data):
        """
        Receive message from client. Calls connect_websocket() method.

        :param text_data: message received from a connected client
        :type text_data: json
        """
        message = json.loads(text_data)
        print('< (client): ', message)
        print('self.channels', self.channels)

        try:
            if 'subscribe' in message['message']:
                client_channels = message['message']['subscribe']

                # Send message to group of currently subbed channels.
                for channel in client_channels:
                    if channel not in self.channels:
                        self.channels.append(channel)
                
                ws_message = {
                    'message': {
                        'subscribe': self.channels
                    }
                }
                self.connect_websocket(json.dumps(ws_message))

        except:
            if message['message'] == 'reset':
                del self.channels[0:]
                print('subscriptions cleared!')
                
                async_to_sync(self.channel_layer.group_send)(
                    self.group_name,
                    {
                        'type': 'client_message',
                        'message': 'subscriptions cleared'
                    }
                )
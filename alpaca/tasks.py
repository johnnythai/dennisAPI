from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import websocket
import json

@shared_task
def test(x, y):
    """
    test function to add 2 numbers
    """
    print(x+y)

@shared_task
def websocket_client(group_name, ws_message):
    """
    Connects to websocket.
    Receives data or channels from websocket.
    Data -> client_message, channels -> consumer_message
    """
    def on_message(ws, message):
        print('< (websocket): ', message)
        jsonMessage = json.loads(message)
        channel_layer = get_channel_layer()

        if 'subscriptions' in jsonMessage['message']:
            async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'consumer_message',
                'message': jsonMessage
            }
        )

        elif 'data' in jsonMessage['message']:
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'client_message',
                    'message': jsonMessage
                }
            )

    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print("### closed ###")

    def on_open(ws):
        print('WEBSOCKET CONNECTION: ', websocket)
        if ws_message != None:
            ws.send(ws_message)
            print('> (websocket): ', ws_message)

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8765",
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close,
                            on_open=on_open)
    ws.run_forever()
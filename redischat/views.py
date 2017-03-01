from django.shortcuts import render
from django.http import HttpResponse
import redis, json
from datetime import datetime as dt
from threading import Thread

CHANNEL_NAME = 'messages'
LISTENER = None

# Create your views here.

class Message:
    """
        Class to hold message details for each
        incoming message
    """
    def __init__(self, payload):
        self.sender = payload['sender']
        self.receiver = payload['receiver']
        self.date = payload['time']
        self.body = payload['message']

class Listener(Thread):
    """
        Threaded class to start client in a separate
        thread which will be dedicated to listen to
        Redis queue, and process each incoming message
    """
    def __init__(self, channel):
        Thread.__init__(self)
        self.redis = redis.Redis()
        self.ps = self.redis.pubsub()
        self.ps.subscribe(channel)
        self.messages = {}

    def storeMessages(self, payload):
        # Store messages in a dict till next 
        # API call is fired
        payload = json.loads(payload)
        message = Message(payload)
        receiver = message.receiver
        if receiver not in self.messages:
            self.messages[receiver] = []
        self.messages[receiver].append(message)

    def getPendingMessages(self, receiver):
        # Retrieve all messages that have reached 
        # since last call. Then clear dict, so 
        # that overhead is not big
        if receiver not in self.messages:
            return []
        messages = self.messages[receiver]
        self.messages[receiver] = []
        return messages

    def run(self):
        # Infinite listener for Redis queue
        for item in self.ps.listen():
            print item
            if item['data'] == 'KILL':
                self.ps.unsubscribe()
                break
            if item['data'] != 1:
                self.storeMessages(item['data'])

def hello(request):
    # Test API endpoint to check if server is running
    return HttpResponse("Hello world, You've successfully reached Django")

def startClient(request):
    # API endpoint to start listener for redis
    global CHANNEL_NAME, LISTENER

    LISTENER = Listener(CHANNEL_NAME)
    LISTENER.start()

    return HttpResponse("Client started successfully")

def stopClient(request):
    # API endpoint to stop listener for redis
    global CHANNEL_NAME
    r = redis.Redis()
    r.publish(CHANNEL_NAME, "KILL")
    return HttpResponse("Client Stopped successfully")

def sendMessage(request):
    # API endpoint to send messages to Redis
    # in JSON format with other params
    global CHANNEL_NAME

    message = request.GET.get('message')
    sender = request.GET.get('sender')
    receiver = request.GET.get('receiver')
    queue = CHANNEL_NAME
    payload = {
        "message": message,
        "sender": sender,
        "receiver": receiver,
        "time": dt.strftime(dt.now(), "%Y-%m-%d %H:%M:%S.%f")
    }
    payload_json = json.dumps(payload)
    r = redis.Redis()
    r.publish(CHANNEL_NAME, payload_json)
    return HttpResponse("Message: {0} has been sent to Redis Queue {1}".format(message, queue))

def getPendingMessages(request):
    # API endpoint to get all pending messages
    # since last call. This will be called as a 
    # long poll
    global LISTENER

    user = request.GET.get('user')
    messages = LISTENER.getPendingMessages(user)
    bodies = [x.body for x in messages]

    return HttpResponse("Messages received: {0}".format(bodies))
from __future__ import unicode_literals

from django.db import models
import redis, json
from threading import Thread

# Create your models here.
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
        sender = message.sender
        if receiver not in self.messages:
            self.messages[receiver] = {}
        if sender not in self.messages[receiver]:
            self.messages[receiver][sender] = []
        self.messages[receiver][sender].append(message)

    def getPendingMessages(self, receiver, sender):
        # Retrieve all messages that have reached 
        # since last call. Then clear dict, so 
        # that overhead is not big
        if receiver not in self.messages:
            return []
        if sender not in self.messages[receiver]:
            return []
        messages = self.messages[receiver][sender]
        self.messages[receiver][sender] = []
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
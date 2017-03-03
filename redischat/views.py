from django.shortcuts import render
from django.http import HttpResponse
import redis, json
from datetime import datetime as dt
import time

from .models import Message, Listener

CHANNEL_NAME = 'messages'
LISTENER = None

# Create your views here.

def hello(request):
    # Test API endpoint to check if server is running
    return HttpResponse("Hello world, You've successfully reached Django")

def test_js(request):
    # Test API endpoint to make sure jQuery is working
    return render(request, "test_js.html")

def landing(request):
    # View to show the landing page
    return render(request, "landing.html")

def chatroom(request):
    # View to show chatroom
    username = request.POST.get("username", "")
    receiver = request.POST.get("receiver", "")
    params = {}
    params['username'] = username
    params['receiver'] = receiver
    return render(request, "chatroom.html", params)


def startClient(request):
    # API endpoint to start listener for redis
    global CHANNEL_NAME, LISTENER

    if LISTENER != None:
        return HttpResponse("Client is already running")

    LISTENER = Listener(CHANNEL_NAME)
    LISTENER.start()

    return HttpResponse("Client started successfully")

def stopClient(request):
    # API endpoint to stop listener for redis
    global CHANNEL_NAME, LISTENER
    r = redis.Redis()
    r.publish(CHANNEL_NAME, "KILL")
    LISTENER = None
    return HttpResponse("Client Stopped successfully")

def sendMessage(request):
    # API endpoint to send messages to Redis
    # in JSON format with other params
    global CHANNEL_NAME

    message = request.GET.get('message')
    sender = request.GET.get('sender')
    receiver = request.GET.get('receiver')
    time = dt.strftime(dt.now(), "%Y-%m-%d %H:%M:%S")
    queue = CHANNEL_NAME
    payload = {
        "message": message,
        "sender": sender,
        "receiver": receiver,
        "time": time
    }
    payload_json = json.dumps(payload)
    r = redis.Redis()
    r.publish(CHANNEL_NAME, payload_json)
    response = {}
    response['success'] = "1"
    response["time"] = time
    response = json.dumps(response)
    return HttpResponse("{0}".format(response))

def getPendingMessages(request):
    # API endpoint to get all pending messages
    # since last call. This will be called as a 
    # long poll
    global LISTENER

    user = request.GET.get('user')
    sender = request.GET.get('sender')
    while True:
        messages = LISTENER.getPendingMessages(user, sender)
        if len(messages) > 0:
            break
        time.sleep(1)
    response = {}
    response['messages'] = []
    for item in messages:
        message = {}
        message['sender'] = item.sender
        message['receiver'] = item.receiver
        message['body'] = item.body
        message['date'] = item.date
        response['messages'].append(message)
    response = json.dumps(response)

    return HttpResponse("{0}".format(response))
from django.shortcuts import render
from django.http import HttpResponse
import redis, json
from datetime import datetime as dt

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
    params = {}
    params['username'] = username
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
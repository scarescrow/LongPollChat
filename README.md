# Django Long Poller

This repo is to explore long polling mechanism. Site is made in Django, and chat messages are sent through a Redis Server.

## Installation

* Install Redis, and start server.
* Clone the project:

```bash
$ git clone https://github.com/scarescrow/LongPollChat.git
```
* Navigate to the cloned folder:
```bash
$ cd LongPollChat
```
* Create a python virtual env. (Optional)
* Install the required packages:
```bash
$ pip install -r requirements.txt
```
* Start the Django Server:
```bash
$ python manage.py runserver
```


####Testing the App:

* Open 2 tabs for http://localhost:8000/redischat in the browser for the 2 clients.
* Enter the username of the sender and receiver in both tabs, and press enter.
* Now both clients are connected. Sending messages from any one should be visible in the other tab and vice versa.


####Note:
1. Currently python connects to default redis server (host=localhost, port=6379). These details are not yet configurable.
2. Polling time for each message is one call per second(provided there is always response). If there is no response, request timeout is 30 seconds, and next poll will be after 2 seconds if there is no response. Also, there is a 1 second sleep time on the server, if there are no messages and it has to check for new messages. 
3. This software supports multiple clients talking to each other in independent chat rooms.
4. Currently there is only one consumer listening to the Redis queue. With increase in traffic, the number of consumers should be increased as well, so that the app scales.

##Current Limitations
1. There is no support for persistent storing of messages in a database, so there is a possibility of messages getting lost.
2. Highly vulnerable to security attacks.


##License

Open sourced under [MIT License](LICENSE)
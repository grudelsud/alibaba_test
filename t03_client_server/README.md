# headaches

mns python sdk is v2.7 only, so...

- a queue manager (can be any language, in this case is python2) sends/receives messages to/from the queue using the mns sdk, then sends the content of the message using a zmq client socket (any language - http://zeromq.org/intro:read-the-manual)
- a msg consumer (python 3) instantiates a zmq server socket and waits for notifications from a client, these containing messages from the queue

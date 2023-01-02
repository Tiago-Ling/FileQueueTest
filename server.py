import socket
from threading import Thread, Lock

SERVER_HOST = "0.0.0.0" # hardcoded local server IP address
SERVER_PORT = 5002 # hardcoded server port

# initialize list/set of all connected client's sockets
# todo: allow multiple clients to connect at the same time and write files to the server
client_sockets = set()

# creates a TCP socket
s = socket.socket()

# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))

# listen for upcoming connections
s.listen(5)

print(f"Listening as {SERVER_HOST}:{SERVER_PORT}")

# create a thread lock to use when appending lines to files
lock = Lock()

# locks the thread, opens the file (creates it if it doesn't exist) and adds the current line to it
def writeToFile(filename, line):
    lock.acquire()
    try:
        f = open(filename, 'a+')  # open file in append mode
        f.write(line)
        f.close()
    finally:
        lock.release()

def addToQueue(filename, line):
    pass

# listens from message from clients, writes lines sent to client-specific files and broadcasts received messages to all connected clients
# todo: receive the filename from clients instead of using the client address
def listen(cs, ca):
    while True:
        try:
            # keep listening for a message from `cs` socket
            msg = cs.recv(1024).decode()
        except Exception as e:
            # client no longer connected
            # remove it from the set
            print(f"Error: {e}")
            client_sockets.remove(cs)
        else:
            # make a thread to write to append lines to a file
            filename = f"{ca}_file.txt"
            file_thread = Thread(target=writeToFile, args=(filename, msg))
            file_thread.start()

        # iterate over all connected sockets and send the latest message to them
        # todo: send messages only to the relevant clients, i.e. the ones interested in the file they sent
        for client_socket in client_sockets:
            ack_msg = f"Writing line to the following file: {filename}"
            client_socket.send(ack_msg.encode())

# main app loop
# todo: implement a way to kill the server for more easily testing it locally
while True:
    # listen for new connections
    client_socket, client_address = s.accept()
    print(f"{client_address} connected.")
    # add new client to the list
    client_sockets.add(client_socket)
    # start a new thread for each new client's messages
    t = Thread(target=listen, args=(client_socket,client_address))
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # starts the thread
    t.start()


# close client sockets
for cs in client_sockets:
    cs.close()
# close server socket
s.close()
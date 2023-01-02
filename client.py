import socket
from threading import Thread, Lock

SERVER_HOST = "127.0.0.1" # hardcoded local server IP address
SERVER_PORT = 5002 # hardcoded server port

# initialize TCP socket
s = socket.socket()
print(f"Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("Connected.")

# creating a thread lock for reading and sending file contents
lock = Lock()

# simply listens for messages from the server, decodes and prints them to the console
def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)

# locks the thread, reads from the file and sends them to the server, line by line
def sendFile(filename):
    lock.acquire()
    try:
        with open(filename) as file:
            while (line := file.readline().rstrip()):
                # todo: fix the issue where the new file created on the server will have an empty line at its end
                s.send((line + "\n").encode())
    finally:
        lock.release()

# make a thread that listens for messages to this client & print them
listen_thread = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
listen_thread.daemon = True
# start the thread
listen_thread.start()

while True:
    # the filename to send to the server
    to_send =  input("Enter filename:")
    # kills the client
    if to_send.lower() == 'q':
        break

    # make a thread to send the file
    filename = to_send
    file_thread = Thread(target=sendFile, args=(filename,))
    file_thread.start()

# close the socket
s.close()
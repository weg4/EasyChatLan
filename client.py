import socket
import threading
import sys
import time
from queue import Queue

message_queue = Queue()

ip_server = ""
port_server = 0

def get_message(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            message_queue.put(message)
        except:
            message_queue.put("Error: Server is disabled")
            break

def print_messages():
    while True:
        message = message_queue.get()
        sys.stdout.write("\r" + " " * 100 + "\r")
        print(message)
        sys.stdout.write("You: ")
        sys.stdout.flush()

def connect_server():
    print("Connecting the server...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip_server, port_server))
        print("Connected the server...")
        threading.Thread(target=get_message, args=(sock, )).start()
        threading.Thread(target=print_messages).start()

        while True:
            message = input()
            sock.send(message.encode('utf-8'))
            sys.stdout.write("You: ")
            sys.stdout.flush()
    except ConnectionRefusedError:
        print("Error: Failed to connect to server")
    finally:
        print("Error: Failed to connect to server")
        time.sleep(10)
        sock.close()
        sys.exit(0)

def settings():
    global port_server, ip_server
    while True: 
        try:
            ip_server = input("Enter server IP: ")
            port_server = int(input("Enter server port: ")) 
            break 
        except:
            print("Error: Please try again")

if __name__ == "__main__":
    settings()
    connect_server()
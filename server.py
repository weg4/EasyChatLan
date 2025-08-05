import socket
import threading

ip = "" # Your local ip.
port = 12345 # Your local port.
password = "" # Your password from local server if nothing is specified there then the user can log in without a paswword.
max_user = 42 # How many users can connect to your local server.
max_name_length = 8 # How many latters can a username have.

client_sock = []
client_info = []

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((ip, port))
    server.listen(max_user)
    print(f"Server started on {ip}:{port}")
    try:
        while True:
            client_socket, addr = server.accept()
            print(f"New user {addr[0]}:{addr[1]}")

            if len(client_sock) >= max_user:
                client_socket.send("Error: Server is full".encode('utf-8'))
                client_socket.close()
                continue
            if user_check(client_socket, addr):
                threading.Thread(target=send_message, args=(client_socket, addr)).start()
                client_sock.append(client_socket)
    except KeyboardInterrupt:
        server.close()

def user_check(client_socket, addr):
    try:
        if password:
            while True:
                client_socket.send("Plesase write password".encode('utf-8'))
                passw = client_socket.recv(1024).decode('utf-8').strip()
                if passw == password:
                    break
                else:
                    client_socket.send("Error: Password failed".encode('utf-8'))
                    continue

        client_socket.send(f"Welcome in {ip}:{port}!\nPlease writes your name, and your name must not contain more than {max_name_length} letters.".encode('utf-8'))
        while True:
            name = client_socket.recv(1024).decode('utf-8').strip()
            if not name:
                continue
            if len(name) > max_name_length:
                client_socket.send("Too long".encode('utf-8'))
                continue
            client_socket.send(f"Everything is fine, now you are in the chat!".encode('utf-8'))
            for client_message in client_sock:
                if client_message != client_socket:
                    client_message.send(f"New user: {addr} - {name}!".encode('utf-8'))
            client_info.append((addr, name))
            return True
    except (ConnectionResetError, OSError):
        print(f"Disconneted: {addr}")
        return False

def send_message(client_socket, addr):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                remove_client(client_socket, addr)
                break
            addr_user = search_client(addr)
            print(f"{addr_user}: {message}")
            for client_message in client_sock:
                if client_message != client_socket:
                    client_message.send(f"{addr_user}:{message}".encode('utf-8'))
        except (ConnectionResetError, OSError):
            remove_client(client_socket, addr)
            break

def search_client(addr):
    for client in client_info:
        if client[0] == addr:
            ip, port = addr
            return f"({ip}:{port}) - {client[1]}"

def remove_client(client_socket, addr):
    print(f"Disconnected {addr}")
    try:
        client_socket.close()
    except:
        pass 
    if client_socket in client_sock:
        client_sock.remove(client_socket)
    for client_ad in client_info:  
        if client_ad[0] == addr:
            client_info.remove(client_ad)
            break  

if __name__ == "__main__":
    start_server()
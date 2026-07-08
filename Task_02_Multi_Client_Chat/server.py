import socket
import select
from datetime import datetime

HOST = '127.0.0.1'
PORT = 5000

# Create TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

print("=================================")
print("   ClassChat Server (Task 02)")
print("=================================")
print(f"Listening on {HOST}:{PORT}")

sockets_list = [server_socket]
clients = {}  # socket: username


def broadcast(message, exclude_socket=None):
    """Send message to all connected clients except sender"""
    for client_socket in list(clients.keys()):
        if client_socket != exclude_socket:
            try:
                client_socket.send(message.encode())
            except:
                remove_client(client_socket)


def remove_client(client_socket):
    """Safely remove disconnected client"""
    if client_socket in clients:
        username = clients[client_socket]
        print(f"{username} disconnected.")
        del clients[client_socket]

        if client_socket in sockets_list:
            sockets_list.remove(client_socket)

        broadcast(f"{username} has left the chat.")
        client_socket.close()


while True:
    read_sockets, _, exception_sockets = select.select(
        sockets_list, [], sockets_list
    )

    for notified_socket in read_sockets:

        # New connection
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            sockets_list.append(client_socket)

            try:
                username = client_socket.recv(1024).decode().strip()
                clients[client_socket] = username

                print(f"{username} connected from {client_address}")

                broadcast(f"{username} has joined the chat.\n")

            except:
                remove_client(client_socket)

        # Existing client sent message
        else:
            try:
                message = notified_socket.recv(1024)

                if not message:
                    remove_client(notified_socket)
                    continue

                username = clients[notified_socket]
                timestamp = datetime.now().strftime("%H:%M:%S")

                formatted_message = f"[{timestamp}] {username}: {message.decode().strip()}"
                print(formatted_message)

                broadcast(formatted_message, notified_socket)

            except:
                remove_client(notified_socket)

    for notified_socket in exception_sockets:
        remove_client(notified_socket)
import socket
import select
import json

HOST = '127.0.0.1'
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

print("=================================")
print("     ClassChat Private Server")
print("=================================")

sockets_list = [server_socket]
clients = {}   # username : socket


def remove_client(client_socket):
    """Safely remove disconnected client"""
    for username, sock in list(clients.items()):
        if sock == client_socket:
            print(f"{username} disconnected.")
            del clients[username]
            break

    if client_socket in sockets_list:
        sockets_list.remove(client_socket)

    client_socket.close()


while True:
    read_sockets, _, exception_sockets = select.select(
        sockets_list, [], sockets_list
    )

    for notified_socket in read_sockets:

        # New connection
        if notified_socket == server_socket:
            client_socket, address = server_socket.accept()
            sockets_list.append(client_socket)

            try:
                username = client_socket.recv(1024).decode().strip()

                # Prevent duplicate usernames
                if username in clients:
                    client_socket.send(
                        json.dumps({
                            "status": "0",
                            "sender": "Server",
                            "receiver": username,
                            "text": "Username already taken."
                        }).encode()
                    )
                    sockets_list.remove(client_socket)
                    client_socket.close()
                else:
                    clients[username] = client_socket
                    print(f"Add new client: {username}")

            except:
                remove_client(client_socket)

        # Existing client message
        else:
            try:
                message = notified_socket.recv(1024)

                # Client disconnected
                if not message:
                    remove_client(notified_socket)
                    continue

                data = json.loads(message.decode())

                sender = data["sender"]
                receiver = data["receiver"]
                text = data["text"]

                print(f"Send from {sender} to {receiver}")

                # Forward message
                if receiver in clients:
                    clients[receiver].send(message)
                else:
                    error_message = {
                        "status": "0",
                        "sender": "Server",
                        "receiver": sender,
                        "text": f"User '{receiver}' not online."
                    }
                    if sender in clients:
                        clients[sender].send(
                            json.dumps(error_message).encode()
                        )

            except Exception as e:
                remove_client(notified_socket)

    for notified_socket in exception_sockets:
        remove_client(notified_socket)
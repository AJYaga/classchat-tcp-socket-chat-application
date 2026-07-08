import socket
import threading

HOST = '127.0.0.1'
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((HOST, PORT))
except:
    print("Unable to connect to server.")
    exit()

username = input("Enter your username: ").strip()
client_socket.send(username.encode())

print("=================================")
print("   Connected to ClassChat")
print("=================================")
print("Type your messages below:")


def receive():
    """Receive messages from server"""
    while True:
        try:
            message = client_socket.recv(1024)

            if not message:
                print("Server disconnected.")
                break

            print("\n" + message.decode())

        except:
            print("Connection closed.")
            break


receive_thread = threading.Thread(target=receive)
receive_thread.daemon = True
receive_thread.start()


while True:
    try:
        message = input()

        if message.lower() == "exit":
            client_socket.close()
            break

        client_socket.send(message.encode())

    except:
        break
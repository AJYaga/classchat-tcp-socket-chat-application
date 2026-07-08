import socket
import threading
import json

HOST = '127.0.0.1'
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

username = input("Enter your username: ").strip()
client_socket.send(username.encode())

print("=================================")
print("     Welcome to ClassChat")
print("=================================")
print("Format: receiver_name: message")
print("Example - Bob: Hello Bob\n")


def receive():
    while True:
        try:
            message = client_socket.recv(1024)

            if not message:
                print("Disconnected from server.")
                break

            data = json.loads(message.decode())

            if data["status"] == "1":
                print(f"\n{data['sender']}: {data['text']}")
            else:
                print(f"\n[Error] {data['text']}")

        except:
            break


thread = threading.Thread(target=receive)
thread.daemon = True
thread.start()


while True:
    msg = input()

    if ":" not in msg:
        print("Invalid format. Use: receiver: message")
        continue

    receiver, text = msg.split(":", 1)

    message_data = {
        "status": "1",
        "sender": username,
        "receiver": receiver.strip(),
        "text": text.strip()
    }

    try:
        client_socket.send(json.dumps(message_data).encode())
    except:
        break
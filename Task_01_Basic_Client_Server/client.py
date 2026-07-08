import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000

def main():
    # Create a TCP socket for communication
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configure TCP protocol with IP address and port number
    server_addr = (SERVER_IP, SERVER_PORT)

    # Connect with server through socket
    client_socket.connect(server_addr)

    # Wait for acknowledgement from server
    ack = client_socket.recv(1024).decode("utf-8").strip()
    print(f"[CLIENT] Server says: {ack}")

    try:
        while True:
            # Send message to the server
            msg = input("[CLIENT] Type message (or 'exit'): ").strip()
            if msg.lower() == "exit":
                break

            client_socket.sendall((msg + "\n").encode("utf-8"))

            # Receive message from server
            reply = client_socket.recv(1024).decode("utf-8").strip()
            print(f"[CLIENT] Reply: {reply}")

    except KeyboardInterrupt:
        print("\n[CLIENT] Closing...")

    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
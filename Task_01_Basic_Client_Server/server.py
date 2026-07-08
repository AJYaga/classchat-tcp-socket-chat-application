import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

def handle_client(conn, addr):
    print(f"[SERVER] Connected by {addr}")

    # Send acknowledgement
    conn.sendall(b"ACK: Connected to ClassChat server\n")

    try:
        while True:
            # Receive message from client
            data = conn.recv(1024)
            if not data:
                print(f"[SERVER] Client {addr} disconnected.")
                break

            msg = data.decode("utf-8").strip()
            print(f"[SERVER] Received from {addr}: {msg}")

            # Send message to client (reply)
            reply = f"Server Reply => I got: {msg}\n"
            conn.sendall(reply.encode("utf-8"))

    finally:
        conn.close()

def main():
    # Create a TCP socket for communication
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Helps avoid "Address already in use" when restarting quickly
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the local port and connection address
    server_socket.bind((HOST, PORT))

    # Listen for client connection
    server_socket.listen(2)
    print(f"[SERVER] Listening on {HOST}:{PORT} ...")

    try:
        while True:
            # Accept connection from client
            conn, addr = server_socket.accept()

            # Handle each client in a separate thread
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down...")

    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
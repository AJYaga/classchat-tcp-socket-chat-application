# ClassChat – TCP/IP Socket-Based Multi-Client Chat Application

## Overview
ClassChat is a terminal-based chat application developed for the EC9590 Network Application Design mini project. It demonstrates TCP/IP socket programming, client-server communication, multi-client handling and private client-to-client messaging.

## Project Tasks

### Task 01 – Basic Client-Server Communication
- Created a TCP server and client.
- Implemented socket creation, binding, listening, accepting connections, acknowledgement, message sending and message receiving.

### Task 02 – Multi-Client Chat
- Extended the server to handle multiple clients.
- Used `select()` for I/O multiplexing.
- Used threading on the client side to allow simultaneous sending and receiving.

### Task 03 – Private Client-to-Client Messaging
- Implemented private messaging through the central server.
- Used JSON messages with sender, receiver, status and text fields.
- Added client management, duplicate username validation and receiver-not-online error handling.

## Technologies Used
- Python
- TCP/IP Sockets
- select()
- threading
- JSON
- Command-Line Interface

## How to Run

Run the server first:

```bash
python server.py
```

Then run one or more clients:

```bash
python client.py
```

For Task 03, send messages using:
receiver_name: message

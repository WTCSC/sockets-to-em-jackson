# server.py

import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clients = []
usernames = {}

def broadcast(message, exclude_client=None):
    for client in clients:
        if client != exclude_client:
            try:
                client.send(message)
            except:
                remove_client(client)

def remove_client(client):
    if client in clients:
        username = usernames.get(client, "Unknown")
        print(f"{username} disconnected.")
        clients.remove(client)
        del usernames[client]
        client.close()
        broadcast(f"[Server] {username} has left the chat.\n".encode())

def handle_client(client):
    try:
        username = client.recv(1024).decode().strip()

        if not username:
            client.close()
            return

        usernames[client] = username
        clients.append(client)

        print(f"{username} connected.")
        broadcast(f"[Server] {username} has joined the chat.\n".encode())

        client.send("[Server] Welcome to the chat!\n".encode())

        while True:
            message = client.recv(1024)

            if not message:
                break

            decoded = message.decode().strip()

            # Command: /users
            if decoded == "/users":
                user_list = ", ".join(usernames.values())
                client.send(f"[Server] Online users: {user_list}\n".encode())
            else:
                broadcast(f"{username}: {decoded}\n".encode(), exclude_client=client)

    except (ConnectionResetError, BrokenPipeError):
        pass
    finally:
        remove_client(client)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server started on {HOST}:{PORT}")
    print("Waiting for connections...\n")

    while True:
        try:
            client, address = server.accept()
            print(f"Connection from {address}")

            thread = threading.Thread(target=handle_client, args=(client,))
            thread.start()

        except KeyboardInterrupt:
            print("\nShutting down server.")
            break

    server.close()

if __name__ == "__main__":
    start_server()
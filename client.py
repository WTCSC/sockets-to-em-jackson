# client.py

import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 5000

def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode()
            if not message:
                print("Disconnected from server.")
                break
            print(message, end="")
        except:
            print("Connection lost.")
            client.close()
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Unable to connect to server.")
        return

    username = input("Enter your username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return

    client.send(username.encode())

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.daemon = True
    receive_thread.start()

    try:
        while True:
            message = input()
            if message.lower() == "/quit":
                break
            if message.strip():
                client.send(message.encode())
    except KeyboardInterrupt:
        pass

    print("Disconnecting...")
    client.close()
    sys.exit()

if __name__ == "__main__":
    start_client()
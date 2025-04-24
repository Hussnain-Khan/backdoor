import socket
from getpass import getpass

SERVER_IP = '127.0.0.1'
SERVER_PORT = 4444

def connect_to_server():
    client = socket.socket()
    print("[CLIENT] Connecting to server...")
    client.connect((SERVER_IP, SERVER_PORT))
    print("[CLIENT] Connected.")

    password = getpass("Enter password: ")
    client.send(password)

    try:
        response = client.recv(1024).strip()
        print("[CLIENT DEBUG] Server responded with: '%s'" % response)
    except Exception as e:
        print("[CLIENT ERROR] Failed to receive response: %s" % str(e))
        client.close()
        return

    if response == "success":
        print("[CLIENT] Login Successful!\n")
    else:
        print("[CLIENT] Login Failed!")
        client.close()
        return

    while True:
        cmd = raw_input(">>> ")
        if cmd.lower() == "exit":
            client.send(cmd)
            break

        if cmd.strip() == "":
            continue

        client.send(cmd)
        result = client.recv(4096)
        print(result)

    client.close()
    print("[CLIENT] Connection closed.")

if __name__ == "__main__":
    connect_to_server()

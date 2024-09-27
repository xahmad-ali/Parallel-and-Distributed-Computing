import socket
import threading

# Function to handle individual client connections
def handle_client(client_socket, address):
    print(f"[+] New connection from {address}")

    while True:
        try:
            # Receive message from client
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received from {address}: {message}")

            # Send a response to the client
            client_socket.send("Message received".encode('utf-8'))

        except ConnectionResetError:
            break

    print(f"[-] Connection from {address} closed")
    client_socket.close()

    #main server function
def start_server():
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0',9999))
    server_socket.listen(5)

    print("[*]Server is listening on port 9999...")

    while True:
        #accept a mew client connection 
        client_socket,addr=server_socket.accept()
        #start a new thread to handle the client
        client_thread=threading.Thread(target=handle_client,args=(client_socket, addr))
        client_thread.start()
if __name__ == "__main__":
    start_server()





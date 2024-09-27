import socket
import threading

# Function to handle individual client connections
def handle_client(client_socket, address):
    print(f"[+] Connected to: {address}")
    print(f"Thread Name, before creating thread: {threading.current_thread().name}")

    while True:
        try:
            # Receive message from client
            mes = client_socket.recv(1024).decode('utf-8')
            print(f"Received from the client: {mes}")

            # Send a response to the client
            response = "Today we will learn about Multithreading with Socket programming"
            client_socket.send(response.encode('utf-8'))

            # Receive the continuation message or 'bye' from the client
            cont = client_socket.recv(1024).decode('utf-8')
            if not cont or cont.lower() == "bye server":
                print("Received from the client: Bye Server")
                break
            else:
                # Send a continuation response to the client
                #response = "Today we will learn about Multithreading with Socket programming"
                client_socket.send(response.encode('utf-8'))

        except ConnectionResetError:
            break

    print(f"[-] Connection from {address} closed.")
    client_socket.close()

# Main server function
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 2022))  # Bind to localhost at port 2022
    server_socket.listen(5)

    print("[*] Server is listening on port 2022...")

    while True:
        # Accept a new client connection
        client_socket, addr = server_socket.accept()
        print(f"New connection: {addr}")

        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr), name=f"Thread-{addr[1]}")
        client_thread.start()

if __name__ == "__main__":
    start_server()

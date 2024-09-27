import socket

# Main client function
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 2022))  # Connect to localhost at port 2022

    try:
        while True:
            # Send a message to the server
            mes = "Hey Server!!! What will we do in today's lab???"
            client_socket.send(mes.encode('utf-8'))
            
            # Receive a response from the server
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Received from the server: {response}")

            # Ask the user if they want to continue
            cont = input("Do you want to continue (y/n): ")
            if cont.lower() != 'y':
                client_socket.send("bye server".encode('utf-8'))
                print("Bye Server")
                break
            else:
                # Send a continuation message
                client_socket.send("continue".encode('utf-8'))
                
                # Receive another response from the server
               # response = client_socket.recv(1024).decode('utf-8')
                #print(f"Received from the server: {response}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()

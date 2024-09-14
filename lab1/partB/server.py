import socket

def start_server(host = '127.0.0.1',port = 8888):
    # Create and config
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"listening at ({host},{port})")

    while True:
        #Accepts a client connection
        client_socket,client_address = server_socket.accept()
        print(f"We have accepted a connection form ({client_address})")

        #display the connected socket
        print(f"Socket connects ({host}, {port}) and ({client_address})")

        #recives 16 oct massage
        client_message_length = client_socket.recv(3).decode()
        client_message = client_socket.recv(1024).decode()
        print(f"the incoming {client_message_length} octet message say {client_message}")

        #send reply to client
        reply_message = "bye bye cleint.."
        client_socket.sendall(reply_message.encode())
        print("Reply sent , socket closed")

        #Close the client sockets
        client_socket.close()

        #listen form an other connection
        print(f"Listeing at ({host}, {port})")

if __name__ == "__main__":
    start_server()
import socket

def run_client(server_host = "127.0.0.1", server_port = 8888 ):
    #Create and config
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Bind to avaliable port
    client_socket.bind(('', 0))
    client_socket.connect((server_host, server_port))

    #get the assigned socket
    client_address = client_socket.getsockname()
    print(f"Client has been assigend socket Name {client_address}")

    #send 16 octet message 
    message = "hello!!"
    message_Len = str(len(message)).zfill(3)
    full = message_Len+message
    print(full)
    client_socket.send(full.encode())

    #recives a respose from the server
    server_message = client_socket.recv(1024).decode()
    print(f"the servre said {server_message}")

    client_socket.close()

if __name__ == "__main__":
    run_client()


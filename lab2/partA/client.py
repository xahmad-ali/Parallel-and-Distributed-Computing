import socket

#main client function
def start_client():
    client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #connect to the server at local host on port 9999
    client_socket.connect(('127.0.0.1',9999))

    try:
        #send a message to the server
        message= input("enter a message to send to the server: ")
        client_socket.send(message.encode('utf-8'))

        #recieve response from the server
        response= client_socket.recv(1024).decode('utf-8')
        print(f"server response: {response}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
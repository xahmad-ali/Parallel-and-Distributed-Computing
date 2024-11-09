import socket

def start_client():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(('127.0.0.1',9999))

    try:
        while True:
            message = input("enter file name : ")
            # client_socket.send(message.encode('utf-8'))
            f = open(message,"r")
            file1 = (f.read())
            client_socket.send(file1.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(f"message from server : {response}")

            message = input("enter file name : ")
            # client_socket.send(message.encode('utf-8'))
            f = open(message,"r")
            file1 = (f.read())
            client_socket.send(file1.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(f"message from server : {response}")

            result = client_socket.recv(1024).decode('utf-8')
            print(f"Multiplication answere is : {result}")

            status = input("do you want to continue? n/y : ")
            if status != 'y':
                message = "bye Server"
                client_socket.send(message.encode('utf-8'))
                break
            else:
                message = "continue"
                client_socket.send(message.encode('utf-8'))

    finally:
        client_socket.close()

if __name__== "__main__":
    start_client()
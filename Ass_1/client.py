import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 9999))


    try:
        file = open("matrixA.txt", "r") 
        m1=  (file.read())
        print(m1)
        file = open("matrixB.txt","r")
        m2 = (file.read())
        client_socket.send((m1).encode('utf-8'))
        response= client_socket.recv(1024).decode('utf-8')
        print(f"server response: {response}")
        client_socket.send((m2).encode('utf-8'))
        response= client_socket.recv(1024).decode('utf-8')
        print(f"server response: {response}")

        calculated= client_socket.recv(1024).decode('utf-8')
        print(calculated)

    finally:
         client_socket.close()



if __name__ == "__main__":
    start_client()
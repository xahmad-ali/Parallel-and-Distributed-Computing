import socket
import threading

def creating_list(message):
    print(message)
    rows=1
    cols=1

    for i in message:
        if i == " ":
            cols+=1
        elif i == "\n":
            break

    for i in message:
        if i == "\n":
            rows+=1
    
    print(f" rows: {rows}\n cols: {cols} ")

    intmessage = list(map(int, message.split()))
    print(intmessage)
    
    matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    index =0 
    for r in range(rows):
        for c in range(cols):
            matrix[r][c] = intmessage[index]
            index+=1

    print(matrix) 
    return matrix,rows,cols

def multiplication(A,B,result,num_row):
    
    for i in range(len(B[0])):
        for j in range(len(B)):
            result[num_row][i] += A[num_row][j] * B[j][i]


def handle_client(client_socket,client_address,server_socket):
    print(f"new connection established {client_address}")

    while True:
        try:
            message1 = client_socket.recv(1024).decode('utf-8')
            if not message1:
                break
            print(f"message from client is -{message1}- on {client_address}")
            client_socket.send("Message recived".encode('utf-8'))
            message2 = client_socket.recv(1024).decode('utf-8')
            if not message2:
                break
            print(f"message from client is -{message2}- on {client_address}")
            client_socket.send("Message recived".encode('utf-8'))

            A,row1,col1= creating_list(message1)
            B,row2,col2 = creating_list(message2)

            result_matrix = [[0 for _ in range(col2)] for _ in range(row1)]
            # print(result_matrix)
            for i in range(row1):
                threads = threading.Thread(target=multiplication, args=(A,B,result_matrix,i))
                threads.start()
            for i in range(row1):
                threads.join()

            client_socket.send(str(result_matrix).encode('utf-8'))

            message = client_socket.recv(1024).decode('utf-8')
            if message != "continue":
                break
        except ConnectionError:
            break
    
    print(f"connection closed from client :{client_address}")
    client_socket.close()
    server_socket.close()


def main_function():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 9999))
    server_socket.listen(5)
    print("server is listening.. on 9999")

    while True:

        client_socket,client_address = server_socket.accept()
        
        client_thread = threading.Thread(target=handle_client , args=(client_socket,client_address,server_socket))
        client_thread.start()    

if __name__ == '__main__':
    main_function()



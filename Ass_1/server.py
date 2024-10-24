import socket
import threading

def matrixing(A,B,result,row):
    print("abc")
    for j in range(0,len(B[0])):
        for k in range(0,len(B)):
            result[row][j] += A[row][k] * B[k][j] 
     
     
     

def shaping(marix):
    #This splits the string marix into a list of substrings using spaces as delimiters.
    #Example: If marix = "12 23 34 45 56 67 78 89 90", then ['12', '23', '34', '45', '56', '67', '78', '89', '90']
    #The map() function returns an iterator, so we use list() to convert this iterator into a list of integers.
    matrix_flat = list(map(int, marix.split()))
    rows=1
    cols=1
    for i in range(len(marix)):
        if(marix[i]=='\n'):
            rows+=1
    print(f"Number of rows: {rows}")
    for i in range(len(marix)):
        if(marix[i]==' '):
            if(marix[i+1]== '\n'):
                    break
            cols+=1
        elif(marix[i]=='\n'):
                break
    print(f"Number of columns: {cols}")

    print(matrix_flat)
    
    print(len(matrix_flat))

    matrix_2d = [[0 for _ in range(cols)] for _ in range(rows)]


    print(matrix_2d)
    
    #(0 -> len matrix, in 3 sublists)
    for i in range(0,len(matrix_flat)):
        row = i // cols   # Calculate the row index
        col = i % cols  
        matrix_2d[row][col] = matrix_flat[i]

    print(matrix_2d)
    return matrix_2d,rows,cols


#########

def backend_processing(client_socket,client_address):
    print(f"[+] New connection from {client_address}")
    try:
        while True:
                matrix1=client_socket.recv(1024).decode('utf-8')
                if not matrix1:
                    break
                print(f"Received from {client_address}:\n{matrix1}")
                client_socket.send("Message received".encode('utf-8'))

                matrix2=client_socket.recv(1024).decode('utf-8')
                if not matrix2:
                    break
                print(f"Received from {client_address}:\n{matrix2}")
                client_socket.send("Message received".encode('utf-8'))
                

                matrixA,rows1,cols1=shaping(matrix1)
                matrixB,rows2,cols2=shaping(matrix2)
                if cols1 == rows2 :
                    print("matrixing\n")
                    result = [[0] * cols2 for _ in range(rows1)]
                    threads=[]
                    for i in range(rows1):
                        thread = threading.Thread(target=matrixing, args=(matrixA,matrixB,result,i))
                        threads.append(thread)
                        thread.start()
                    
                    for thread in threads:
                        thread.join()
                    
                    print(f"Result:\n{result}")
                    client_socket.send(str(result).encode('utf-8'))
                else:
                     client_socket.send("Matrix multiplication not possible".encode('utf-8'))
                    
                    

    except Exception as e:
        print(e)
    finally:
        print(f"[-] Connection from {client_address} closed")
        client_socket.close()
        


def start_server():
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0",9999))
    server_socket.listen(5)
    print("[*]Server is listening on port 9999...")

    while True:
        client_socket,client_address=server_socket.accept()
        threads= threading.Thread(target=backend_processing, args=(client_socket,client_address))
        threads.start()
        

    


if __name__ == "__main__":
    start_server()
    
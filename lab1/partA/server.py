# server.py
import socket

# Create a TCP socket (SOCK_STREAM for TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to an address and port
server_socket.bind(('localhost', 12345))

# Listen for incoming connections (queue up to 5 connections)
server_socket.listen(5)
print("Server is listening...")

# Accept a client connection
client_socket, client_address = server_socket.accept()
print(f"Connection established with {client_address}")

# Receive and send data
message = client_socket.recv(1024).decode()  # Receive 1024 bytes of data
print(f"Received from client: {message}")
client_socket.send("Hello, Client!".encode())  # Send a response to the client

# Close the connection
client_socket.close()
server_socket.close()
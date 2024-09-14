#Client Side
import socket

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server (using localhost and port 12345)
client_socket.connect(('localhost', 12345))

# Send a message to the server
client_socket.send("Hello, Server!".encode())

# Receive a response from the server
response = client_socket.recv(1024).decode()
print(f"Received from server: {response}")

# Close the connection
client_socket.close()
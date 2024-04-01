import socket
import threading
import sys

#defininf the server ip and port
SERVER_IP = "localhost"
SERVER_PORT = 12345

#function to receive messages from server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(16000).decode()
            print(message)
        except:
            client_socket.close()
            sys.exit()

#function to send messages to server
def send_message(client_socket):
    while True:
        try:
            message = input()
            client_socket.send(message.encode())
            #condition for exiting the chatroom
            if message == "/exit":
                client_socket.close()
                sys.exit()
        except:
            client_socket.close()
            sys.exit()

#main function
if __name__ == "__main__":  
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, SERVER_PORT))
    #creating threads for sending and receiving messages
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()
    send_thread = threading.Thread(target=send_message, args=(client,))
    send_thread.start()

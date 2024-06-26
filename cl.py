import socket
import threading
import sys
import ipaddress

#defining the server ip and port
SERVER_IP = ""
SERVER_PORT = 12345

#defining a thread lock object
lock = threading.Lock()

#function to receive messages from server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(16000).decode()
            lock.acquire()
            print(message)
            lock.release()
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
    
def check_ip(ip):
    try:
        ipaddress.IPv4Network(ip)
        return True
    except ValueError:
        return False

#main function
if __name__ == "__main__":
    print("Please enter ip address of the server:")
    SERVER_IP = input()
    while check_ip(SERVER_IP) == False:
        print("Please enter a valid ip address:")
        SERVER_IP = input()
    #creating a socket object  
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, SERVER_PORT))
    #creating threads for sending and receiving messages
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()
    send_thread = threading.Thread(target=send_message, args=(client,))
    send_thread.start()
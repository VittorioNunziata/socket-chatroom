#importing libraries
import socket
import threading 
import random

#defining server ip and port
SERVER_NANE=socket.gethostname()
SERVER_IP = socket.gethostbyname(SERVER_NANE)
SERVER_PORT = 12345

#dictionary to store clients
clients = {}

#list of default colors in ANSI format
colors = ["\033[91m",  # Red
          "\033[92m",  # Green
          "\033[93m",  # Yellow
          "\033[94m",  # Blue
          "\033[95m",  # Magenta
          "\033[96m"   # Cyan
          ]

#dictionary of commands
commands = {"changeu":"changeu <username> let the user change username",
            "changecol":"changecol <color number> let the user change color seen by others", 
            "users":"print all online users", 
            "help":"display all commands", 
            "exit":"exit the chatroom"
            }

#list of default usernames
names = ["Banana",
         "Apple",
         "Grape",
         "XxxDarkAngelCraftxxX",
         "Pineapple",
         "Matteo_Messina_Denaro"
         ]

#list of users online
users_online = []

#function to broadcast messages to all clients
def broadcast(message, sender_socket):
    sender_color = clients[sender_socket][1] 
    sender_name = clients[sender_socket][0]
    for client_socket, (name, color) in clients.items():
        if client_socket != sender_socket:
            try:
                client_socket.send(f"{sender_color}{sender_name}: {message}\033[0m".encode())
            except:
                del clients[client_socket]

#function to handle clients
def handle_client(client_socket,client_address):
    client_socket.send("Welcome to the Chatroom!".encode())
    client_socket.send("From now you can chat with other people in the Chat".encode())
    #defining variable to store messages
    msgcli = ""
    #assigning random username and color to client
    client_name = random.choice(names)
    users_online.append(client_name)
    names.remove(client_name)
    client_color = random.choice(colors)
    colors.remove(client_color)
    while True:
        try:
            message = client_socket.recv(16000).decode()
            if message:
                #checking if message is a command
                if message.startswith("/"):
                    command = message.split(" ")[0]
                    match command:
                        #case to change username
                        case "/changeu":
                            try:
                                new_name = message.split(" ")[1]
                                #checking if new username is not already taken or empty
                                if new_name.isspace() == False and new_name != "" and new_name not in users_online:
                                    print("changed username to: ", new_name)
                                    users_online.remove(client_name)
                                    client_name = new_name 
                                    users_online.append(client_name)
                                else:
                                    msgcli = "invalid username, please choose a different one"
                                    client_socket.send(msgcli.encode())
                            except:
                                msgcli = "invalid username, please follow the syntax: /changeu <new_username>"
                                client_socket.send(msgcli.encode())
                        #case to change color assigned to user     
                        case "/changecol":
                            try:
                                new_color = message.split(" ")[1]
                                new_color = int(new_color)
                                if new_color > 0 and new_color <= 255:
                                    print("changed color of user"+client_name+"to: ", new_color)
                                    client_color = "\033[38;5;" + str(new_color) + "m"
                                else:
                                    msgcli = "invalid color number, please choose a color between 1 and 255"
                                    client_socket.send(msgcli.encode())
                            except:
                                msgcli = "invalid color number, please follow the syntax: /changecol <color_number>"
                                client_socket.send(msgcli.encode())
                        #case to display all users online
                        case "/users":
                            client_socket.send("Users online: ".encode())
                            for user in users_online:
                               msgcli = user
                               client_socket.send(msgcli.encode())
                        #case to display all commands
                        case "/help":
                            client_socket.send("Commands: \n".encode())
                            for key, value in commands.items():
                                msgcli ="/"+key + " : " + value +"\n"
                                client_socket.send(msgcli.encode())
                        #case to exit the chatroom       
                        case "/exit":
                            print("closing connection with", client_address , flush=True)
                            print("Done", flush=True)
                            client_socket.close()
                            break
                        #case default for invalid commands
                        case _:
                            msgcli = "invalid command, type /help to see all commands"
                            client_socket.send(msgcli.encode())
                #condition for messages who are not commands
                else:
                    clients[client_socket] = (client_name, client_color)
                    broadcast(message, client_socket)                 
        except:
            del clients[client_socket]
            client_socket.close()
            break

#function to accept connections from clients
def accept_connections():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen()
    print(f"Server listening on {SERVER_IP}:{SERVER_PORT}", flush=True)
    while True:
        client_socket, client_address = server.accept()
        print(f"Connection from {client_address} has been established.", flush=True)
        #creating a thread for each client
        thread = threading.Thread(target=handle_client, args=(client_socket,client_address,))
        thread.start()

#main function
if __name__ == "__main__":
    accept_connections()
import socket
import threading

HOST = '127.0.0.1'  
# ipconfig on cmd fr ur owm IP address
# for public IP Address visit sites like - myip.is
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []




# ----------- broadcast --------------
def broadcast(message):
    for client in clients:
        client.send(message)



# ------------ handle -----------------
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break



# ----------- receive ----------------
def receive():
    while True:
        # accept new connection i.e. new client
        client, address = server.accept()
        print(f"Connected with {str(address)}!")

        # ask for nickname of client
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)

        # add nickname of client to clients list
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} connected to server!\n".encode('utf-8'))
        client.send("Connected to the server".encode('utf-8'))  #send msg to particular client

        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()

print("Server running..")
receive()
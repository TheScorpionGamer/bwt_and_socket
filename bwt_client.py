import socket

#AF_INET     --> IPv4
#SOCK_STREAM --> TCP

ip = "127.0.0.1" # localhost
port = 5281    # porta locale

#socket.connect((ip,port)) # fa richiesta di connessione al server

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((ip,port))
print(f"Connesso al server: {ip}:{port}")

print("BWT - Client e Server")
phrase = input("Inserisci la frase da trasformare con BWT\n")

client_socket.sendall(phrase.encode("utf-8"))
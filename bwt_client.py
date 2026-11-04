import socket

#AF_INET     --> IPv4
#SOCK_STREAM --> TCP

ip = "127.0.0.1" # localhost
port = 5281    # porta locale

#socket.connect((ip,port)) # fa richiesta di connessione al server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket: # guarda bwt_server.py per capire cos'è il with (riga 41)

    client_socket.connect((ip,port))
    print(f"Connesso al server: {ip}:{port}")

    print("BWT - Client e Server")
    phrase = input("Inserisci la frase da trasformare con BWT\n")

    client_socket.sendall(phrase.encode("utf-8"))

    data = client_socket.recv(2048) # ricevi massimo 2048byte di informazioni
    answer = data.decode("utf-8")
    print(f"Risposta ricevuta dal server: {answer}")
import socket
from bwt import bwt

#AF_INET     --> IPv4
#SOCK_STREAM --> TCP

ip = "127.0.0.1" # localhost
port = 5281    # porta locale
exit_phrase = "you should shutdown now" # frase per chiudere il server

#socket.bind((ip,port)) # collega al socket ip e port
#socket.listen()      # resta in attesa di richieste
#socket.accept()      # accetta la richiesta

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((ip,port))

while True:
    server_socket.listen()
    print(f"Server in ascolto all'IP: {ip}:{port}")

    client_socket, client_address = server_socket.accept()
    print(f"Client trovato, Address: {client_address}")

    data = client_socket.recv(2048) # ricevi massimo 2048byte di informazioni
    phrase = data.decode("utf-8")
    print(f"Frase ricevuta: {phrase}")

    if phrase.lower() == exit_phrase:
        print("Ricevuto comando di arresto del server.")
        client_socket.sendall("Server in fase di arresto, come richiesto.".encode("utf-8"))
        client_socket.close()
        break

    answer = bwt(phrase)
    print(f"Frase inviata: {answer}")

    client_socket.sendall(answer.encode("utf-8")) # invia la risposta al client

    client_socket.close() # chiudi la connessione con il client
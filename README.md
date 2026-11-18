# Burrows-Wheeler Transform

Progetto Python per il calcolo della **Burrows-Wheeler Transform (BWT)** e per la sua esecuzione attraverso una comunicazione **client-server tramite socket TCP**.

Il progetto è diviso in due parti:

1. implementazione dell'algoritmo BWT;
2. comunicazione client-server, dove il client invia una stringa al server e riceve indietro la stringa trasformata.

---

## Parte 1 — Burrows-Wheeler Transform

La **Burrows-Wheeler Transform** è una trasformazione che riordina i caratteri di una stringa in modo da raggruppare caratteri simili tra loro.

La trasformazione non comprime direttamente i dati, ma può essere utilizzata come passaggio preliminare per rendere più efficaci alcuni algoritmi di compressione.

### Funzionamento

Prendiamo come esempio la stringa:

```text
Banana
```

### 1. Aggiunta del carattere `$`

Alla fine della stringa viene aggiunto il carattere speciale `$`, utilizzato per indicare la fine della stringa.

```text
Banana$
```

---

### 2. Generazione delle rotazioni

Vengono generate tutte le possibili rotazioni della stringa.

Ad ogni passaggio, il primo carattere viene spostato alla fine:

```text
Banana$
Anana$b
Nana$ba
Ana$ban
na$bana
a$banan
$banana
```

Il numero di rotazioni generate è uguale al numero di caratteri della stringa dopo l'aggiunta di `$`.

---

### 3. Ordinamento lessicografico

Le rotazioni vengono successivamente ordinate in ordine lessicografico.

Il carattere `$` ha precedenza rispetto alle lettere.

```text
1. $banana
2. a$banan
3. ana$ban
4. anana$b
5. banana$
6. na$bana
7. nana$ba
```

Nel programma l'ordinamento viene realizzato confrontando i caratteri delle stringhe e utilizzando un algoritmo di ordinamento manuale.

---

### 4. Creazione della BWT

Una volta ordinate le rotazioni, viene preso **l'ultimo carattere di ogni riga**:

```text
$banan │ a
a$bana │ n
ana$ba │ n
anana$ │ b
banana │ $
na$ban │ a
nana$b │ a
       │
       └──► annb$aa
```

La trasformata di Burrows-Wheeler della stringa `banana` è quindi:

```text
annb$aa
```

Nel programma questa operazione viene effettuata scorrendo tutte le rotazioni ordinate e concatenando il loro ultimo carattere.

---

## Struttura dell'algoritmo

Il programma segue quindi questi passaggi:

```text
Stringa originale
       │
       ▼
Aggiunta di "$"
       │
       ▼
Generazione delle rotazioni
       │
       ▼
Ordinamento lessicografico
       │
       ▼
Estrazione dell'ultima colonna
       │
       ▼
Risultato BWT
```

La trasformazione è contenuta in una funzione che riceve la stringa da trasformare e restituisce il risultato della BWT.

Questo permette di utilizzare lo stesso algoritmo anche nella seconda parte del progetto.

---

# Parte 2 — Client e Server TCP

Nella seconda parte del progetto la trasformazione BWT viene eseguita attraverso una comunicazione di rete.

Sono utilizzati due programmi:

- **Client** — richiede all'utente la stringa da trasformare e la invia al server;
- **Server** — riceve la stringa, calcola la Burrows-Wheeler Transform e restituisce il risultato al client.

La comunicazione utilizza dei **socket TCP**.

---

## Comunicazione

Il funzionamento generale è:

```text
             "banana"
CLIENT ─────────────────► SERVER
                            │
                            │
                            ▼
                       BWT("banana")
                            │
                            ▼
                        "annb$aa"
                            │
CLIENT ◄────────────────────┘
            "annb$aa"
```

Il client non esegue direttamente la trasformazione: invia solamente la stringa al server e attende la risposta.

Il server si occupa invece dell'elaborazione.

---

## Socket TCP

Per la comunicazione vengono utilizzati socket:

```python
socket.AF_INET
socket.SOCK_STREAM
```

`AF_INET` indica l'utilizzo di **IPv4**, mentre `SOCK_STREAM` indica l'utilizzo del protocollo **TCP**.

Per i test client e server vengono eseguiti sullo stesso computer utilizzando:

```text
IP:    127.0.0.1
Porta: 5281
```

`127.0.0.1` corrisponde a **localhost**.

---

## Funzionamento del server

Il server segue principalmente questi passaggi:

```text
socket()
   │
   ▼
bind()
   │
   ▼
listen()
   │
   ▼
accept()
   │
   ▼
recv()
   │
   ▼
BWT
   │
   ▼
sendall()
```

### `bind()`

Associa il socket a un indirizzo IP e a una porta.

### `listen()`

Mette il server in ascolto in attesa di connessioni.

### `accept()`

Accetta la connessione proveniente da un client.

### `recv()`

Riceve i dati inviati dal client.

Il server utilizza quindi la stringa ricevuta come input della funzione BWT.

### `sendall()`

Il risultato della trasformazione viene infine inviato al client.

---

## Funzionamento del client

Il client segue invece:

```text
socket()
   │
   ▼
connect()
   │
   ▼
input()
   │
   ▼
sendall()
   │
   ▼
recv()
   │
   ▼
output
```

Il client crea un socket TCP e utilizza `connect()` per collegarsi all'indirizzo e alla porta del server.

Dopo la connessione:

1. richiede all'utente la stringa;
2. invia la stringa al server;
3. attende il risultato;
4. mostra la BWT ricevuta.

---

## Codifica dei dati

I socket non inviano direttamente stringhe Python, ma sequenze di **byte**.

Prima dell'invio una stringa viene quindi convertita utilizzando:

```python
.encode("utf-8")
```

Il destinatario esegue l'operazione inversa:

```python
.decode("utf-8")
```

Il flusso dei dati è quindi:

```text
"banana"
   │
   │ encode()
   ▼
b'banana'
   │
   │ TCP
   ▼
b'banana'
   │
   │ decode()
   ▼
"banana"
```

La stessa operazione viene effettuata quando il server restituisce al client il risultato della trasformazione.

---

# Struttura del progetto

```text
BWT/
│
├── bwt.py
├── client.py
├── server.py
└── README.md
```

### `bwt.py`

Contiene l'algoritmo della Burrows-Wheeler Transform:

- aggiunta di `$`;
- generazione delle rotazioni;
- confronto lessicografico;
- ordinamento;
- estrazione dell'ultima colonna;
- restituzione del risultato.

### `server.py`

Crea il server TCP, riceve la stringa dal client, utilizza la funzione BWT e restituisce il risultato.

### `client.py`

Si connette al server, richiede una stringa all'utente, la invia e mostra il risultato ricevuto.

---

# Esecuzione

Per utilizzare la versione client-server è necessario avviare prima il server:

```bash
python server.py
```

Il server rimarrà in ascolto in attesa di una connessione.

Successivamente, in un secondo terminale, viene avviato il client:

```bash
python client.py
```

Il client richiederà la stringa da trasformare.

Esempio:

```text
Inserisci la frase da trasformare con BWT:
banana
```

La stringa viene inviata al server, che esegue la trasformazione e restituisce:

```text
annb$aa
```

---

## Obiettivo del progetto

Il progetto permette di applicare due concetti differenti:

- implementazione della **Burrows-Wheeler Transform** e dell'ordinamento lessicografico;
- utilizzo dei **socket TCP** per realizzare una semplice architettura client-server.

Il risultato finale permette quindi di eseguire la trasformazione BWT su un server a partire da una stringa inserita sul client.
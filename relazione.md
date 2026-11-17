# Burrows-Wheeler Transform integrato ad archittetura Client-Server - Laboratorio di Informatica

**Autore:** Claudio Carlotti
**Istituto di Istruzione Superiore "Archimede" – Treviglio**

---

## Abstract

In questa esperienza è stata realizzata in Python un'applicazione client-server basata su socket TCP che calcola la Burrows-Wheeler Transform (BWT) di una frase. Il client acquisisce una frase da tastiera e la invia al server; il server calcola la BWT mediante una funzione implementata a mano (generazione di tutte le rotazioni della stringa, ordinamento lessicografico con un confronto scritto da zero e selezione dell'ultima colonna) e restituisce il risultato al client, che lo mostra a video. Il server può inoltre essere arrestato da remoto inviando una frase di arresto predefinita. Sono stati verificati il corretto funzionamento della comunicazione sulla rete locale e la correttezza della trasformazione su alcuni esempi.

## Introduzione

Lo scopo dell'esperienza è unire due argomenti: la **programmazione di rete** con i socket e un **algoritmo di trasformazione di stringhe**, la Burrows-Wheeler Transform. La BWT riordina i caratteri di un testo in modo da raggruppare quelli uguali, e per questo è usata nella compressione dei dati (ad esempio in bzip2) e nella bioinformatica.

La comunicazione tra i due programmi avviene tramite socket TCP (`SOCK_STREAM`) su IPv4 (`AF_INET`), scelti perché TCP garantisce un canale affidabile e ordinato tra client e server. Il linguaggio utilizzato è **Python**, scelto per la sintassi concisa e per il modulo `socket` della libreria standard, che permette di scrivere un server e un client in poche righe. Il server e il client girano entrambi sulla stessa macchina, all'indirizzo di loopback `127.0.0.1`, sulla porta `5281`.

Il progetto è composto da tre file:

- `bwt.py`: contiene l'algoritmo della BWT;
- `bwt_server.py`: il server, che riceve le frasi e risponde con la loro trasformata;
- `bwt_client.py`: il client, che invia la frase e mostra la risposta.

*Pagine consultate:* W3Schools e Python Documentation, oltre alle spiegazioni e alle slide dei professori.

## Materiale e metodi

### Strumenti

- Linguaggio: Python v3.13.2
- IDE: Visual Studio Code
- Librerie: `socket` e `bwt`, quest'ultima è fatta custom dal sottoscritto (`bwt.py`).

### La Burrows-Wheeler Transform (`bwt.py`)

L'algoritmo si svolge in quattro passi:

1. **Aggiunta del carattere terminatore.** Alla frase viene aggiunto il carattere `$`, che segna la fine del testo e rende la trasformazione reversibile.
2. **Generazione delle rotazioni.** Per ogni indice `i` si costruisce la rotazione ciclica della stringa:

   ```python
   for i in range(len(bwt_phrase)):
       bwt_versions.append(bwt_phrase[i:] + bwt_phrase[:i])
   ```

3. **Ordinamento lessicografico.** Invece di usare `sorted()`, l'ordinamento è stato scritto a mano con l'algoritmo **selection sort**. Per decidere quale di due stringhe viene prima è stata scritta la funzione `isInOrder(version, version2)`, che confronta le stringhe carattere per carattere: al primo carattere diverso restituisce `True` se il carattere della prima è minore, `False` se è maggiore; se le stringhe sono uguali restituisce `False`.

   ```python
   for i in range(len(bwt_order)):
       minimo = i
       for j in range(i + 1, len(bwt_order)):
           if isInOrder(bwt_order[j], bwt_order[minimo]):
               minimo = j
       tmp = bwt_order[i]
       bwt_order[i] = bwt_order[minimo]
       bwt_order[minimo] = tmp
   ```

   L'ordinamento viene eseguito su una copia della lista (`.copy()`), altrimenti le due variabili punterebbero alla stessa lista in memoria.

4. **Estrazione dell'ultima colonna.** Il risultato è la stringa formata dall'ultimo carattere di ciascuna rotazione ordinata (`version[-1]`).

### Il server (`bwt_server.py`)

Il server è composto da un ciclo `while True` che, a ogni iterazione:

1. crea un socket TCP con `socket.socket(AF_INET, SOCK_STREAM)` all'interno di un blocco `with`, che garantisce la chiusura automatica del socket;
2. lo collega a IP e porta con `bind((ip, port))` e si mette in ascolto con `listen(5)` (fino a 5 client in coda);
3. accetta una connessione con `accept()`, che restituisce il socket del client e il suo indirizzo;
4. riceve i dati con `recv(2048)` (massimo 2048 byte) e li decodifica in UTF-8;
5. se la frase ricevuta (in minuscolo) coincide con la **frase di arresto** `"you should shutdown now"`, risponde con un messaggio di conferma, chiude la connessione e interrompe il ciclo con `break`;
6. altrimenti calcola `bwt(phrase)` e invia il risultato al client con `sendall()`, codificandolo in UTF-8.

### Il client (`bwt_client.py`)

Il client crea un socket TCP, si connette al server con `connect((ip, port))`, legge la frase da tastiera con `input()`, la invia con `sendall()` dopo averla codificata in UTF-8, attende la risposta con `recv(2048)` e la stampa a video. Anche qui il blocco `with` chiude il socket automaticamente al termine.

## Risultati e discussione

Il sistema funziona come previsto: avviando prima `bwt_server.py` e poi `bwt_client.py`, il client si connette, invia la frase e riceve la sua trasformata di Burrows-Wheeler.

**Esempio di funzionamento.** Per la frase `banana` il server costruisce la stringa `banana$` e ne genera le rotazioni, che una volta ordinate sono:

| Rotazioni ordinate | Ultimo carattere |
|--------------------|:----------------:|
| `$banana` | `a` |
| `a$banan` | `n` |
| `ana$ban` | `n` |
| `anana$b` | `b` |
| `banana$` | `$` |
| `na$bana` | `a` |
| `nana$ba` | `a` |

Il risultato è quindi `annb$aa`: si nota come i caratteri uguali (`a`, `n`) tendano a raggrupparsi, ed è proprio questa la proprietà che rende la BWT utile per la compressione. *(Verificare l'esempio eseguendo il programma e, se si vuole, aggiungere uno screenshot dell'output di client e server.)*

**Perché il codice si comporta così.** Il carattere `$` ha un codice ASCII (36) inferiore a quello delle lettere, quindi nel confronto risulta sempre prima di queste e la rotazione che inizia con `$` finisce in prima posizione. Il confronto di `isInOrder` si basa sul codice dei caratteri, perciò maiuscole e minuscole non sono equivalenti (le maiuscole precedono le minuscole).

**Limiti e osservazioni.**

- **Efficienza.** Il selection sort esegue circa n² confronti e ogni confronto può costare fino a n operazioni, quindi l'algoritmo è adatto a frasi brevi ma diventa lento su testi lunghi; `sorted()` di Python sarebbe molto più veloce.
- **Dimensione dei messaggi.** `recv(2048)` limita la frase a 2048 byte e non garantisce di ricevere tutto il messaggio in una sola chiamata.
- **Un client alla volta.** Il server gestisce una sola connessione per ciclo, quindi serve i client uno dopo l'altro.
- **Carattere `$` nella frase.** Se la frase contiene già `$`, la trasformazione non è più univocamente invertibile.
- **Confronto della frase di arresto.** Viene applicato `.lower()` solo alla frase ricevuta, quindi il comando di arresto funziona con qualsiasi combinazione di maiuscole e minuscole.

## Conclusione

L'obiettivo è stato raggiunto: è stata realizzata un'applicazione client-server funzionante in cui il client invia una frase e il server restituisce la sua Burrows-Wheeler Transform, calcolata con un algoritmo scritto interamente a mano. L'esperienza ha permesso di comprendere il funzionamento dei socket TCP (`bind`, `listen`, `accept`, `connect`, `sendall`, `recv`) e di mettere in pratica algoritmi di ordinamento e confronto tra stringhe. Come possibili sviluppi si potrebbero implementare la trasformata inversa, la gestione di più client contemporanei (ad esempio con i thread) e un ordinamento più efficiente.

## Bibliografia

Fonti consultate per ricavare informazioni e pezzi di codice:

- La Burrows-Wheeler Transform e i socket sono stati spiegati dai professori Piccolo Gianluca e Mazzocca Antonio, che hanno fornito anche le slide usate come riferimento.
- [W3Schools](https://www.w3schools.com)
- [Python Docs](https://docs.python.org/3.12/)

# !/usr/bin/env python3

import socket
import sys
import threading
import random #Genera numeros aleatorios

####################3################# PARTE BUSCAMINAS ##############################################

#Funcion que imprime tablero
def imprimirTablero(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            print(matriz[i][j], end=" ")
        print()
    print()

# tableroServidor


#Mis funciones a emplear
def generarTableroServidor(n, dificultad, minas):
    if dificultad == 'f':
        tableroCabecera = [" ","A","B","C","D","E","F","G","H","I"]
        tableroColumna = [" ", 0,1,2,3,4,5,6,7,8]
    else:
        tableroCabecera = [" "," A","B","C","D","E","F","G","H","I", "J", "K", "L", "M","N", "O", "P"]
        tableroColumna = [" ", " 0"," 1"," 2"," 3"," 4"," 5"," 6"," 7"," 8"," 9",10,11,12,13,14,15]
    tableroServidor = [[ "*" for x in range(n+1)] for x in range(n+1)]
    for i in range(1):
        for j in range(len(tableroServidor[i])):
            if tableroServidor[i][j] == "*":
                tableroServidor[i][j] = tableroCabecera[j]
                tableroServidor[j][i] = tableroColumna[j]
    #Vamos a insertar las minas de forma aleatoria
    incremento = 0
    while incremento < minas:
        posX = random.randint(2, n)
        posY = random.randint(2, n)
        if tableroServidor[posX][posY] == "*":
            tableroServidor[posX][posY] = "M"
            incremento+=1
    return tableroServidor

def generarTableroCliente(n, dificultad):
    if dificultad == 'f':
        tableroCabecera = [" ","A","B","C","D","E","F","G","H","I"]
        tableroColumna = [" ", 0,1,2,3,4,5,6,7,8]
    else:
        tableroCabecera = [" "," A","B","C","D","E","F","G","H","I", "J", "K", "L", "M","N", "O", "P"]
        tableroColumna = [" ", " 0"," 1"," 2"," 3"," 4"," 5"," 6"," 7"," 8"," 9",10,11,12,13,14,15]
    tableroCliente = [[ "*" for x in range(n+1)] for x in range(n+1)]
    for i in range(1):
        for j in range(len(tableroCliente[i])):
            if tableroCliente[i][j] == "*":
                tableroCliente[i][j] = tableroCabecera[j]
                tableroCliente[j][i] = tableroColumna[j]
    return tableroCliente

def verificarToqueMina(tableroServidor, CooX, CooY):
    #Buscamos el numero de la letra para obtener la coordenada de la mina
    for i in range(1):
        for j in range (len(tableroServidor[i])):
            if tableroServidor[i][j].strip() == CooY:
                CooY = j
    if tableroServidor[CooX+1][CooY] == "M":
        print(" *** El cliente ha tocado una mina :( *** ")
        return 1
    else:
        return 0

def actualizarTableroCliente(tableroCliente, numero, letra, toque):
    CooYN = 0
    CooXN = 0
    if toque == 0:
        #Hallo el numero
        for i in range(len(tableroCliente)):
            for j in range(1):
                if tableroCliente[i][j] == numero:
                    CooXN = i
        #Hallo la letra
        for i in range(1):
            for j in range(len(tableroCliente)):
                if tableroCliente[i][j] == " A":
                    CooYN = j    
                if tableroCliente[i][j] == letra:
                    CooYN = j
        tableroCliente[CooXN][CooYN] = "-"
    else:
        tableroCliente[CooXN][CooYN] = "X"
    return tableroCliente

####################################### FIN BUSCAMINAS ###############################################


####################3################# PARTE HILO SERVIDOR ##############################################
def obtenerNombreHilo():
    return threading.current_thread().name

def servirPorSiempre(socketTcp, listaconexiones):
    try:
        while True:
            client_conn, client_addr = socketTcp.accept()
            print("Conectado a", client_addr)
            listaconexiones.append(client_conn)
            thread_read = threading.Thread(target=recibir_datos, args=[client_conn, client_addr])
            thread_read.start()
            # print("La lista: ",len(listaConexiones))
            # if listaConexiones < len(listaConexiones):
            gestion_conexiones(listaConexiones)
            # else:
            #     print("No se puede recibir otra conexión")
    except Exception as e:
        print(e)

def gestion_conexiones(listaconexiones):
    for conn in listaconexiones:
        if conn.fileno() == -1:
            listaconexiones.remove(conn)
    print("hilos activos:", threading.active_count())
    print("enum", threading.enumerate())
    print("conexiones: ", len(listaconexiones))
    # print("Lista de conexiones: ",listaconexiones)


def recibir_datos(conn, addr):
    global tableroCliente
    global tableroServidor
    try:
        cur_thread = threading.current_thread()
        print("Recibiendo datos del cliente {} en el {}".format(addr, cur_thread.name))
        while True:
            data = conn.recv(1024)
            #Verificamos si el cliente quiere un juego o partida con la dificultad para crearlo sino que reciba las coordenadas
            recibidoCliente = data.decode()
            nombreHilo = obtenerNombreHilo()
            if (recibidoCliente.lower() == "jugar" or recibidoCliente.lower() == "f" or recibidoCliente.lower() == "d") and nombreHilo[0:8] == "Thread-1":
                #Solicita la dificultad
                if recibidoCliente.lower() == "jugar":
                    # print("Jugó")
                    response = "Ingrese la dificultad del juego: "
                    response = response.encode()
                else:
                    #Generar tablero
                    print("Se generará el tablero del cliente {} en el {}".format(addr, cur_thread.name))
                    if recibidoCliente.lower() == "f":
                        print("Modo fácil")
                        dificultad = "f"
                        tableroServidor = generarTableroServidor(9, dificultad, 10)
                        #Visualizamos el tablero del servidor
                        imprimirTablero(tableroServidor)
                        #creamos el tablero del cliente el cual vamos a pasar
                        tableroCliente = generarTableroCliente(9, dificultad)
                        #Enviar tablero cliente
                        response = tableroCliente
                        # print(response)
                        responseT = str(response).encode('utf-8')
                        response = bytearray(responseT)
                        print("Se envio el tablero, verifica en el lado del cliente")
                    else:
                        print("Modo difícil")
                        dificultad = "d"
                        tableroServidor = generarTableroServidor(16, dificultad, 40)
                        #Visualizamos el tablero del servidor
                        imprimirTablero(tableroServidor)
                        #creamos el tablero del cliente el cual vamos a pasar
                        tableroCliente = generarTableroCliente(16, dificultad)
                        #Enviar tablero cliente
                        response = tableroCliente
                        # print(response)
                        responseT = str(response).encode('utf-8')
                        response = bytearray(responseT)
                        tableroClienteEnvio = response
                        print("Se envio el tablero, verifica en el lado del cliente")
            elif (recibidoCliente.lower() == "jugar" or recibidoCliente.lower() == "f" or recibidoCliente.lower() == "d") and nombreHilo[0:8] != "Thread-1":
                response = "Ya existe una partida, por lo cual se unira al juego"
                response = response.encode()
                print(response)
            elif recibidoCliente.lower() == "si":
            #Enviar tablero cliente
                response = tableroCliente
                responseT = str(response).encode('utf-8')
                response = bytearray(responseT)
                tableroClienteEnvio = response
                print("Se le envió el tablero al cliente {} en el {}".format(addr, cur_thread.name))
            elif recibidoCliente.lower() == "no":
                print("El cliente no quiere unirse a la partida actual")
                print("Se cerrará su conexión")
                response = "bye"
            elif recibidoCliente[:recibidoCliente.find(",")].isdigit() and recibidoCliente[recibidoCliente.find(",")]==',' and type(recibidoCliente[recibidoCliente.find(",")+1:]) is str:
                print("Recibimos la coordenada {} del cliente {} en el {}".format(recibidoCliente,addr, cur_thread.name))
                numeroTablero = recibidoCliente[:recibidoCliente.find(",")]
                numeroTablero = int(numeroTablero)
                letraTablero = recibidoCliente[recibidoCliente.find(",")+1:].upper()
                #Actualizo el tablero del cliente
                tableroCliente = actualizarTableroCliente(tableroCliente,numeroTablero, letraTablero, 0)
                #Enviar tablero cliente
                response = tableroCliente
                responseT = str(response).encode('utf-8')
                response = bytearray(responseT)
                tableroClienteEnvio = response
                #Checo si toqué una mina
                tocoMina = verificarToqueMina(tableroServidor, numeroTablero, letraTablero.upper())
                # print("toco mina: ", tocoMina)
                if tocoMina != 1:
                    print("No tocó una mina")
                    # #Envio que no ha tocado mina
                    #Respondo con tablero
                    response = tableroClienteEnvio
                else:
                    response = "Ha tocado una mina, GAME OVER"
                    response = response.encode()
            elif data.decode()!="bye":#If para coordenadas
                response = input("Ingrese el mensaje a enviar: ").encode()
            else:
                print("El cliente solicitó cerrar la conexión")
            if not data:
                print("Fin.")
                break
            conn.sendall(response)
    except Exception as e:
        print(e)
    finally:
        conn.close()
        print("Se cerró la conexión\nEsperando otra conexión...")



##Parte principal
mensajeInicio = """
        ========================================
        *************** SERVIDOR ***************
        ========================================
"""
print(mensajeInicio)
listaConexiones = []
# host, port, numConn = sys.argv[1:4]

# if len(sys.argv) != 4:
#     print("usage:", sys.argv[0], "<host> <port> <num_connections>")
#     sys.exit(1)
# host = input("Ingrese el host: ")
# port = input("Ingrese el puerto: ")
host = "localhost"
port = 12345
numConn = 4

serveraddr = (host, int(port))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    tableroServidor = []
    tableroCliente = []
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind(serveraddr)
    TCPServerSocket.listen(int(numConn))
    print("El servidor TCP está disponible y en espera de solicitudes")

    servirPorSiempre(TCPServerSocket, listaConexiones)
#!/usr/bin python3

import socket
import json #Dar formato del arreglo

HOST = "127.0.0.1"  # Hostname o  dirección IP del servidor
PORT = 12345  # Puerto del servidor
buffer_size = 1024 #Tamaño de los datos que recibe
existeTablero = 0 #Para saber si ya recibimos el tablero
data = b'' #Variable de data

def imprimirTablero(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            print(matriz[i][j], end=" ")
        print()
    print()

def receive_all(sock):
    """Recibe todos los datos del socket"""
    data = b""
    while True:
        part = sock.recv(1024)
        data += part
        if len(part) < 1024:
            break
    return data

def formatoTabla(dataB):
    #Ahorta vamos a darle el formato para imprimirlo en la pantalla
    cadenaBytesTablero = dataB.decode()
    #Le damos el formato de JSON válido con comillas dobles no simples
    # Reemplazamos las comillas simples por dobles
    cadenaBytesTablero = cadenaBytesTablero.replace("'", '"')
    # Convertimos el string a una lista bidimensional de Python utilizando json.loads()
    cadenaTablero = json.loads(cadenaBytesTablero)
    # Imprimimos la lista para verificar que el proceso fue exitoso y mostrarselo al cliente
    return cadenaTablero

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    #Para guardar el tablero
    cadenaTablero = ""
    TCPClientSocket.connect((HOST, PORT))
    print("Enviando mensaje...")
    mensaje = "jugar"
    print("Recibido,", repr(data), " de", TCPClientSocket.getpeername())
    while mensaje!="bye":
        recibirTablero = 0
        #Mensaje para el input por defecto
        mensajeInput = "Ingrese el mensaje:\t"
        TCPClientSocket.sendall(mensaje.encode())
        print("Esperando una respuesta...")
        # Para recibir completo el arreglo en bytes
        #Generamos una funcion que reciba todo el mensaje por si es de mayor longitud
        data = receive_all(TCPClientSocket)
        
        dataB = bytearray(data)
        datop = dataB.decode()
        if datop.find("existe") != -1:
            print("Recibido,", repr(data), " de", TCPClientSocket.getpeername())
            recibirTablero = 1
        elif len(dataB)>0 and data.decode().find("GAME OVER") == -1:
            if chr(dataB[0]) == '[' or chr(dataB[1])=='[':
                if existeTablero == 0:
                    #Recibo el tablero porque tiene la estructura de la lista bidimensional 
                    cadenaTablero = formatoTabla(dataB)
                    #Lo imprimimos
                    imprimirTablero(cadenaTablero)
                    existeTablero = 1
                elif existeTablero >= 1:
                    #Recibo el tablero porque tiene la estructura de la lista bidimensional 
                    cadenaTablero = formatoTabla(dataB)
                    #Lo imprimimos
                    imprimirTablero(cadenaTablero)
                    existeTablero += 1
                else:
                    print("Se genero un problema con el tablero")
        elif data.decode().find("GAME OVER") != -1:
            print("Recibido,", repr(data), " de", TCPClientSocket.getpeername())
            print("Pisó una mina :(\nFin del juego")
            print("Cerrando conexión...")
            break
        else:
            print("Recibido,", repr(data), " de", TCPClientSocket.getpeername())

        if not data or dataB == "bye":
            break
    
        if recibirTablero == 1:
            mensaje = input("Desea jugar? si/no\t")
        elif existeTablero >= 1:
            mensajeInput = "Ingrese las coordenadas en el formato (No,L), ejem: \'5,A\'\t"
            mensaje = input(mensajeInput)
        else:
            mensaje = input(mensajeInput)
    print("\nSe cerró la conexión fin")
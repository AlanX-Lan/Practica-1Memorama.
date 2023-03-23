# Elaborado por Trinidad González Alan Isaac
import socket
import time

# Crear un objeto socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Solicitar al usuario que ingrese el host y el puerto para la conexión del socket
HOST = input("Ingresa el host del servidor: ")
PORT = int(input("Ingresa el puerto del servidor: "))

# Conectarse al servidor
client_socket.connect((HOST, PORT))
print("Conectado al servidor.")

# Solicitar al usuario que elija la dificultad del juego
difficulty = input("Elige la dificultad del juego (facil o dificil): ")
client_socket.sendall(difficulty.encode())

# Jugar al memorama
while True:
    # Solicitar al usuario que elija dos cartas del memorama
    card_1 = input("Ingresa la posición de la primera carta (por ejemplo, '01' para la carta en la fila 0, columna 1), o escribe 'exit' para salir: ")
    if card_1 == 'exit':
        client_socket.sendall(card_1.encode())
        response = client_socket.recv(1024).decode()
        print(response)
        break
    client_socket.sendall(card_1.encode())
    card_2 = input("Ingresa la posición de la segunda carta (por ejemplo, '23' para la carta en la fila 2, columna 3): ")
    client_socket.sendall(card_2.encode())

    # Recibir la respuesta del servidor
    response = client_socket.recv(1024).decode()
    print(response)

    # Si el servidor envía un mensaje de finalización, salir del juego
    if response.startswith("¡Felicidades!"):
        end_time = time.time()
        elapsed_time = round(end_time - start_time, 2)
        print(f"¡Felicidades! Has completado el memorama en {elapsed_time} segundos.")
        break

# Cerrar el socket
client_socket.close()
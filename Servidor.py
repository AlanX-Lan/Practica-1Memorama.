# Elaborado por Trinidad González Alan Isaac
import socket
import random
import time

# Configurar el servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Solicitar al usuario que ingrese el host y el puerto para la conexión del socket
HOST = input("Ingresa el host para el servidor: ")
PORT = int(input("Ingresa el puerto para el servidor: "))

# Vincular el servidor al host y al puerto especificados
server_socket.bind((HOST, PORT))

# Escuchar las conexiones entrantes
server_socket.listen(1)
print(f"Servidor escuchando en {HOST}:{PORT}")

# Aceptar una conexión entrante
connection, address = server_socket.accept()
print(f"Conexión establecida desde {address}.")

# Recibir la dificultad del juego del cliente
difficulty = connection.recv(1024).decode()
print(f"Dificultad del juego: {difficulty}")

# Definir el tamaño del tablero del memorama según la dificultad
if difficulty == "facil":
    BOARD_SIZE = 4
elif difficulty == "dificil":
    BOARD_SIZE = 6

# Crear el tablero del memorama
values = list(range(1, (BOARD_SIZE*BOARD_SIZE)//2 + 1)) * 2
random.shuffle(values)
board = [[0] * BOARD_SIZE for i in range(BOARD_SIZE)]
for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):
        board[i][j] = values.pop()

# Jugar al memorama
start_time = time.time()
matches = 0
while matches < BOARD_SIZE*BOARD_SIZE//2:
    # Enviar el tablero actual al cliente
    board_str = ""
    for row in board:
        row_str = " ".join([str(val) if val != 0 else "-" for val in row])
        board_str += row_str + "\n"
    connection.sendall(board_str.encode())

    # Recibir la posición de la primera carta del cliente
    card_1_pos = connection.recv(1024).decode()
    if card_1_pos == "exit":
        connection.sendall("¡Juego cancelado por el usuario!".encode())
        break
    card_1_row, card_1_col = int(card_1_pos[0]), int(card_1_pos[1])

    # Recibir la posición de la segunda carta del cliente
    card_2_pos = connection.recv(1024).decode()
    card_2_row, card_2_col = int(card_2_pos[0]), int(card_2_pos[1])

    # Comprobar si las cartas son iguales
    if board[card_1_row][card_1_col] == board[card_2_row][card_2_col]:
        matches += 1
        board[card_1_row][card_1_col] = 0
        board[card_2_row][card_2_col] = 0
        message = "¡Cartas iguales! "
        if matches == BOARD_SIZE*BOARD_SIZE//2:
            message += "¡Felicidades! Has completado el memorama."
        else:
            message += f"Llevas {matches} de {BOARD_SIZE*BOARD_SIZE//2} parejas encontradas."
    else:
        message = "¡Cartas diferentes! Sigue intentando."

    # Enviar la respuesta al cliente
    connection.sendall(message.encode())

# Cerrar la conexión
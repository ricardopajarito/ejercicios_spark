from random import randint

intentos = 0
estimado = 0
numero_secreto = randint(1, 100)

nombre = input("Ingrese su nombre: ")
print(f"Bienvenido, {nombre}! Estoy pensando en un número entre 1 y 100.\nTienes 8 intentos para adivinarlo")

while intentos < 8:
    estimado = int(input(f"Intento {intentos + 1}: Adivina el número: "))
    intentos += 1

    if estimado not in range(1, 101):
        print("El número debe estar entre 1 y 100. Inténtalo de nuevo.")
    elif estimado < numero_secreto:
        print("El número es mayor. Inténtalo de nuevo.")
    elif estimado > numero_secreto:
        print("El número es menor. Inténtalo de nuevo.")
    else:
        print(f"Felicitaciones, {nombre}! Adivinaste el número en {intentos + 1} intentos.")
        break

if estimado != numero_secreto:
    print(f"Lo siento, {nombre}. El número secreto era {numero_secreto}.")
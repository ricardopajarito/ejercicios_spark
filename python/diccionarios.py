# Diccionario de un producto
producto = {
    "nombre": "Laptop HP",
    "precio": 850,
    "stock": 23,
    "disponible": True
}

# Diccionario vacío
datos = {}

# También se puede crear así
persona = dict(nombre="Ana", edad=30, ciudad="Madrid")

# Acceder a un elemento
print(producto["precio"])


producto = {"nombre": "Laptop", "precio": 850}

# Forma 1: Corchetes (lanza error si no existe)
print(producto["nombre"])  # → Laptop
print(producto["marca"])   # → KeyError! ❌

# Forma 2: .get() (devuelve None o un valor por defecto)
print(producto.get("nombre"))        # → Laptop
print(producto.get("marca"))         # → None
print(producto.get("marca", "Sin marca"))  # → Sin marca


Python
producto = {"nombre": "Laptop", "precio": 850}

# Agregar una clave nueva
producto["marca"] = "HP"
# → {"nombre": "Laptop", "precio": 850, "marca": "HP"}

# Modificar un valor existente
producto["precio"] = 799
# → {"nombre": "Laptop", "precio": 799, "marca": "HP"}

# Eliminar una clave
del producto["marca"]
# → {"nombre": "Laptop", "precio": 799}

# Eliminar y obtener el valor
precio = producto.pop("precio")
# precio = 799, producto = {"nombre": "Laptop"}

producto = {"nombre": "Laptop", "precio": 850, "stock": 23}

# Iterar solo claves
for clave in producto:
    print(clave)
# → nombre, precio, stock

# Iterar solo valores
for valor in producto.values():
    print(valor)
# → Laptop, 850, 23

# Iterar claves y valores (LA MÁS USADA)
for clave, valor in producto.items():
    print(f"{clave}: {valor}")
# → nombre: Laptop
# → precio: 850
# → stock: 23


# Datos de un pedido (típico de una API)
pedido = {
    "id": 1234,
    "cliente": {
        "nombre": "María García",
        "email": "[email protected]"
    },
    "productos": [
        {"nombre": "Laptop", "precio": 850},
        {"nombre": "Mouse", "precio": 25}
    ],
    "total": 875
}

# Acceder a datos anidados
print(pedido["cliente"]["nombre"])  # → María García
print(pedido["productos"][0]["nombre"])  # → Laptop

# Forma segura (por si falta alguna clave)
email = pedido.get("cliente", {}).get("email", "No disponible")

ventas = ["laptop", "mouse", "laptop", "teclado", "laptop", "mouse"]

contador = {}
for producto in ventas:
    contador[producto] = contador.get(producto, 0) + 1

print(contador)
# → {"laptop": 3, "mouse": 2, "teclado": 1}

estados = {
    "P": "Pendiente",
    "E": "En proceso",
    "C": "Completado",
    "X": "Cancelado"
}

codigo = "E"
print(f"Estado: {estados[codigo]}")
# → Estado: En proceso

empleados = [
    {"nombre": "Ana", "depto": "Ventas"},
    {"nombre": "Luis", "depto": "IT"},
    {"nombre": "María", "depto": "Ventas"},
]

por_depto = {}
for emp in empleados:
    depto = emp["depto"]
    if depto not in por_depto:
        por_depto[depto] = []
    por_depto[depto].append(emp["nombre"])

print(por_depto)
# → {"Ventas": ["Ana", "María"], "IT": ["Luis"]}
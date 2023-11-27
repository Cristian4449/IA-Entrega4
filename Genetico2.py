import random

# Lista de productos en el supermercado con sus precios
productos_precios = {
    "Leche entera": 2.5,
    "Pan": 1.0,
    "Huevos": 3.0,
    "Cebolla": 1.5,
    "Tomate": 1.2,
    "Manzana": 1.0,
    "Aguacate": 2.1,
    "Pera": 0.9,
    "Naranja": 0.5,
    "Papa negra": 1.7,
    "Papa amarilla": 1.5,
    "Carne de res": 7.0,
    "Pasta": 1.8,
    "Salsa": 2.2,
    "Arroz": 1.3,
    "Aceite": 3.5,
    "Aceite oliva": 9.0,
    "Leche deslactosada": 5.0,
    "Carne de cerdo": 10.1,
    "Pollo": 8.5,
    "Chorizo": 12.5,
    "Sal": 4.0,
    "Azúcar": 3.9,
    "Brocoli": 1.2,
    "Panela": 7.9,
    "Chocolate": 6.8,
    "Cafe": 5.9,
    "Harina": 3.1,
}

# Crear una población inicial de posibles listas de compras
def generar_poblacion(tamano_poblacion, num_productos, productos):
    poblacion = []
    for _ in range(tamano_poblacion):
        cromosoma = random.sample(productos, num_productos - 2)  
        productos_prioritarios = random.sample(["Leche entera", "Carne de res"], 2)  
        cromosoma.extend(productos_prioritarios) 
        poblacion.append(cromosoma)
    return poblacion

# Función de aptitud: evalúa la conveniencia de la lista basándose en precios
def evaluar_poblacion(poblacion, precios):
    return [sum(precios[producto] for producto in lista) for lista in poblacion]

# Seleccionar dos padres al azar
def seleccionar_padres(poblacion):
    return random.sample(poblacion, 2)

# Cruzar dos listas de compras para producir dos descendientes
def cruzar(padre1, padre2):
    punto_cruce = random.randint(0, len(padre1) - 1)
    hijo1 = padre1[:punto_cruce] + [gen for gen in padre2 if gen not in padre1[:punto_cruce]]
    hijo2 = padre2[:punto_cruce] + [gen for gen in padre1 if gen not in padre2[:punto_cruce]]
    return hijo1, hijo2

# Mutar una lista de compras cambiando dos productos de lugar
def mutar(individuo):
    puntos_muta = random.sample(range(len(individuo)), 2)
    individuo[puntos_muta[0]], individuo[puntos_muta[1]] = individuo[puntos_muta[1]], individuo[puntos_muta[0]]
    return individuo

# Algoritmo genético completo
def algoritmo_genetico(tamano_poblacion, tasa_mutacion, generaciones, num_productos):
    productos = list(productos_precios.keys())
    
    poblacion = generar_poblacion(tamano_poblacion, num_productos, productos)
    puntuaciones = evaluar_poblacion(poblacion, productos_precios)

    for generacion in range(generaciones):
        aptitud_maxima = max(puntuaciones)
        aptitud_promedio = sum(puntuaciones) / len(puntuaciones)
        mejor_lista = poblacion[puntuaciones.index(aptitud_maxima)]
        
        print(f'\nGeneración {generacion + 1}: {mejor_lista}, \nAptitud Máxima: {aptitud_maxima}, \nAptitud Promedio: {aptitud_promedio}')

        nueva_generacion = []

        for _ in range(tamano_poblacion // 2):
            padre1, padre2 = seleccionar_padres(poblacion)
            hijo1, hijo2 = cruzar(padre1, padre2)

            if random.random() < tasa_mutacion:
                print(f'Mutación en individuo: {hijo1}')
                hijo1 = mutar(hijo1)
            if random.random() < tasa_mutacion:
                print(f'Mutación en individuo: {hijo2}')
                hijo2 = mutar(hijo2)

            nueva_generacion.extend([hijo1, hijo2])

        poblacion = nueva_generacion
        puntuaciones = evaluar_poblacion(poblacion, productos_precios)

# Ejemplo de uso:
tamano_poblacion = 10
tasa_mutacion = 0.5
generaciones = 10
num_productos = 5

algoritmo_genetico(tamano_poblacion, tasa_mutacion, generaciones, num_productos)

import random

# Lista de productos en el supermercado
productos = ["leche", "pan", "huevos", "frutas", "verduras", "carne", "pasta", "salsa", "arroz", "aceite"]

# Crear una población inicial de posibles listas de compras
def generar_poblacion(tamano_poblacion, productos):
    return [random.sample(productos, len(productos)) for _ in range(tamano_poblacion)]

# Función de aptitud: en este caso, evalúa la conveniencia de la lista basándose en preferencias
def evaluar_poblacion(poblacion, preferencias):
    return [sum(preferencias[producto] for producto in lista) for lista in poblacion]

# Seleccionar dos padres basados en la ruleta ponderada
def seleccionar_padres(poblacion, puntuaciones):
    return random.choices(poblacion, weights=puntuaciones, k=2)

# Cruzar dos listas de compras para producir dos descendientes
def cruzar(padre1, padre2):
    punto_cruce = random.randint(0, len(padre1) - 1)
    hijo1 = padre1[:punto_cruce] + [gen for gen in padre2 if gen not in padre1[:punto_cruce]]
    hijo2 = padre2[:punto_cruce] + [gen for gen in padre1 if gen not in padre2[:punto_cruce]]
    return hijo1, hijo2

# Mutar una lista de compras cambiando dos productos de lugar
def mutar(individuo):
    punto_muta = random.sample(range(len(individuo)), 2)
    individuo[punto_muta[0]], individuo[punto_muta[1]] = individuo[punto_muta[1]], individuo[punto_muta[0]]
    return individuo

# Algoritmo genético completo
def algoritmo_genetico(tamano_poblacion, tasa_mutacion, generaciones):
    for generacion in range(generaciones):
        # Generar preferencias aleatorias en cada iteración
        preferencias_usuario = {producto: random.randint(1, 10) for producto in productos}

        poblacion = generar_poblacion(tamano_poblacion, productos)
        puntuaciones = evaluar_poblacion(poblacion, preferencias_usuario)

        mejor_lista = poblacion[puntuaciones.index(max(puntuaciones))]
        print(f'\nGeneración {generacion + 1}: {mejor_lista}, \nAptitud: {max(puntuaciones)}, \nPreferencias: {preferencias_usuario}')

        nueva_generacion = []

        for _ in range(tamano_poblacion // 2):
            padre1, padre2 = seleccionar_padres(poblacion, puntuaciones)
            hijo1, hijo2 = cruzar(padre1, padre2)

            if random.random() < tasa_mutacion:
                hijo1 = mutar(hijo1)
            if random.random() < tasa_mutacion:
                hijo2 = mutar(hijo2)

            nueva_generacion.extend([hijo1, hijo2])

        poblacion = nueva_generacion

# Ejemplo de uso:
tamano_poblacion = 100
tasa_mutacion = 0.1
generaciones = 10

algoritmo_genetico(tamano_poblacion, tasa_mutacion, generaciones)
import random
from deap import base, creator, tools, algorithms
import numpy
import matplotlib.pyplot as plt

# Lista de productos y precios
productos_precios = {
    "Leche entera": 2.5,"Pan": 1.0,
    "Huevos": 3.0,"Cebolla": 1.5,
    "Tomate": 1.2,"Manzana": 1.0,
    "Aguacate": 2.1,"Pera": 0.9,
    "Naranja": 0.5,"Papa negra": 1.7,
    "Papa amarilla": 1.5, "Carne de res": 7.0,
    "Pasta": 1.8, "Salsa": 2.2,
    "Arroz": 1.3, "Aceite": 3.5,
    "Aceite oliva": 9.0, "Leche deslactosada": 5.0,
    "Carne de cerdo": 10.1, "Pollo": 8.5,
    "Chorizo": 12.5, "Sal": 4.0,
    "Azúcar": 3.9, "Brocoli": 1.2,
    "Panela": 7.9, "Chocolate": 6.8,
    "Cafe": 5.9, "Harina": 3.1,
}
# Lista para almacenar estadísticas
avg_stats = []
min_stats = []
max_stats = []

# Presupuesto máximo
PRESUPUESTO_MAXIMO = 20  #Cambiar según sea necesario

# Crear tipos de Fitness y Individuo
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# Función para inicializar individuos
def create_individual():
    return [random.randint(0, 1) for _ in productos_precios]

toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Función de evaluación
def evaluar_individuo(individual):
    total_cost = sum(individual[i] * price for i, price in enumerate(productos_precios.values()))
    return (total_cost,) if total_cost <= PRESUPUESTO_MAXIMO else (0,)

toolbox.register("evaluate", evaluar_individuo)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

# Función para imprimir detalles de cada individuo
def print_individual_details(individual, productos_precios, flag = False):
    productos_seleccionados = [producto for producto, selected in zip(productos_precios.keys(), individual) if selected]
    costo_total = sum(productos_precios[producto] for producto in productos_seleccionados)
    if flag:
        print(f"Productos: {productos_seleccionados} - Costo: ${costo_total} ")
    else:
        print(f"Individuo: {individual} - Costo: ${costo_total}")

# Parámetros del algoritmo genético
size_of_population = 80
number_of_generations = 100

# Crear población
pop = toolbox.population(n=size_of_population)
hof = tools.HallOfFame(1)

stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean)
stats.register("min", numpy.min)
stats.register("max", numpy.max)

# Ejecutar el algoritmo genético con impresión de detalles de cada individuo
for gen in range(number_of_generations):
    offspring = algorithms.varAnd(pop, toolbox, cxpb=0.5, mutpb=0.2)
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit

    pop = toolbox.select(offspring, k=len(pop))

    record = stats.compile(pop)
    avg_stats.append(record["avg"])
    min_stats.append(record["min"])
    max_stats.append(record["max"])
    
    # Imprimir detalles de cada individuo en la generación actual
    print(f"\nGeneración {gen + 1}")
    for ind in pop:
        print_individual_details(ind, productos_precios)

    # Actualizar Hall of Fame
    hof.update(pop)
# Graficar estadísticas
gen_range = range(1, number_of_generations + 1)
plt.figure(figsize=(10, 6))
plt.plot(gen_range, avg_stats, label="Promedio")
plt.plot(gen_range, min_stats, label="Mínimo")
plt.plot(gen_range, max_stats, label="Máximo")
plt.xlabel("Generación")
plt.ylabel("Costo")
plt.title("Evolución del Costo a lo largo de las Generaciones")
plt.legend()
plt.grid(True)
plt.show()

# Mejor individuo
mejor_individuo = hof[0]
print("\nMejor cromosoma final (representación binaria):", mejor_individuo)
print_individual_details(mejor_individuo, productos_precios, True)

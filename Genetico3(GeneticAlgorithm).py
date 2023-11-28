import random
from geneticalgorithm import geneticalgorithm as ga
import numpy as np

# Datos del problema
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

limite_presupuesto = 20.0  # Puedes ajustar este valor según tu presupuesto

# Función de aptitud (fitness) que se debe minimizar
def fitness_function(X):
    productos_seleccionados = [productos_precios[producto] for producto, seleccionado in zip(productos_precios.keys(), X) if seleccionado]
    precio_total = sum(productos_seleccionados)
    excedido_presupuesto = max(0, precio_total - limite_presupuesto)
    return excedido_presupuesto

# Configuración del algoritmo genético
varbound = np.array([[0, 1]] * len(productos_precios))  # Cada variable binaria indica si se selecciona o no un producto

algorithm_param = {'max_num_iteration': 50, 'population_size': 50, 'mutation_probability': 0.5, 'elit_ratio': 0.1,
                   'crossover_probability': 0.5, 'crossover_type': 'two_point', 'max_iteration_without_improv': None,
                   'parents_portion': 0.5}  # Ajusta esta proporción según tus necesidades

model = ga(function=fitness_function, dimension=len(productos_precios), variable_type='bool', variable_boundaries=varbound,
           algorithm_parameters=algorithm_param)

# Ejecutar el algoritmo evolutivo
model.run()

# Obtener el mejor individuo y su aptitud
best_solution = model.output_dict['variable']
best_fitness = fitness_function(best_solution)

# Imprimir resultados
print("\nMejor conjunto de productos seleccionados:")
for i, (producto, seleccionado) in enumerate(zip(productos_precios.keys(), best_solution)):
    if seleccionado:
        print(f"{i + 1}. {producto}")

precio_total_seleccionado = sum(productos_precios[producto] for producto, seleccionado in zip(productos_precios.keys(), best_solution) if seleccionado)
print("Precio total seleccionado:", precio_total_seleccionado)
print("Presupuesto excedido:", best_fitness)

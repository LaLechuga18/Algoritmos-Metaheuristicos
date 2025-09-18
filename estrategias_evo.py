import numpy as np
import matplotlib.pyplot as plt

# --- DEFINICION DE LAS FUNCIONES A OPTIMIZAR ---
def funcion_1(x):
    x0, x1 = x[0], x[1]
    return x0 * np.exp(-x0**2 - x1**2)

def funcion_2(x):
    return np.sum(np.square(x))

# --- ALGORITMO DE ESTRATEGIA EVOLUTIVA ---
def estrategia_evolutiva(funcion_objetivo, limites, D, mu, la, G):
    # 1. Inicializacion
    poblacion = []
    for _ in range(mu):
        individuo = {
            'posicion': np.random.uniform(limites[0], limites[1], D),
            'sigma': np.random.rand(D) * 0.5 # Tasa de mutacion inicial
        }
        poblacion.append(individuo)

    mejor_solucion_global = None
    mejor_fitness_global = float('inf')
    historial_fitness = []

    print(f"--- Iniciando optimizacion para '{funcion_objetivo}' ---")
    
    # 2. Ciclo Evolutivo
    for gen in range(G):
        descendencia = []
        # 3. Creacion de descendencia
        for _ in range(la):
            # Seleccionar dos padres al azar de la poblacion
            padre1, padre2 = np.random.choice(poblacion, 2, replace=False)
            
            # Recombinacion sexual discreta
            hijo_pos = np.zeros(D)
            hijo_sigma = np.zeros(D)
            for i in range(D):
                if np.random.rand() < 0.5:
                    hijo_pos[i] = padre1['posicion'][i]
                    hijo_sigma[i] = padre1['sigma'][i]
                else:
                    hijo_pos[i] = padre2['posicion'][i]
                    hijo_sigma[i] = padre2['sigma'][i]

            # Se muta la tasa de mutacion (sigma) y luego la posicion
            hijo_sigma = hijo_sigma * np.exp(np.random.randn(D) / np.sqrt(D))
            hijo_pos = hijo_pos + hijo_sigma * np.random.randn(D)
            
            # Asegurar que el hijo este dentro de los limites
            hijo_pos = np.clip(hijo_pos, limites[0], limites[1])
            
            descendencia.append({'posicion': hijo_pos, 'sigma': hijo_sigma})

        # 4. Evaluacion y Seleccion
        pool_combinado = poblacion + descendencia
        
        # Calcular el fitness para cada individuo en el pool
        fitness_pool = [funcion_objetivo(ind['posicion']) for ind in pool_combinado]
        
        # Ordenar los individuos por su fitness (de menor a mayor)
        indices_ordenados = np.argsort(fitness_pool)
        
        # Los 'mu' mejores sobreviven para la siguiente generación
        poblacion = [pool_combinado[i] for i in indices_ordenados[:mu]]

        # Actualizar la mejor solucion encontrada hasta ahora
        mejor_fitness_generacion = fitness_pool[indices_ordenados[0]]
        if mejor_fitness_generacion < mejor_fitness_global:
            mejor_fitness_global = mejor_fitness_generacion
            mejor_solucion_global = poblacion[0]['posicion']
            
        if (gen + 1) % 10 == 0:
            print(f"Generacion {gen+1}/{G} | Mejor Fitness: {mejor_fitness_global:.5f}")
        historial_fitness.append(mejor_fitness_global)

    return mejor_solucion_global, mejor_fitness_global, historial_fitness


# --- EJECUCION ---
# Parametros
D = 2
miu = 20
lamb = 100
gen = 100

# Resultados para la funcion 1
limites_f1 = [-2, 2]
# Captura el 'historial_f1' que ahora devuelve la funcion
mejor_pos_f1, mejor_val_f1, historial_f1 = estrategia_evolutiva(funcion_1, limites_f1, D, miu, lamb, gen)

print("\n--- Resultados Finales funcion 1 ---")
print(f"Minimo conocido en: [-0.70711, 0] con valor -0.42888")
print(f"Minimo encontrado en: [{mejor_pos_f1[0]:.5f}, {mejor_pos_f1[1]:.5f}] con valor {mejor_val_f1:.5f}\n")

# --- GRAFICA FUNCION 1 ---
plt.figure()
plt.plot(historial_f1, color='blue')
plt.title("Convergencia para funcion 1")
plt.xlabel("Generacion")
plt.ylabel("Mejor Fitness")
plt.grid(True)
plt.show() 

# **Resultados para la funcion 2**
limites_f2 = [-5.12, 5.12]
# Captura el 'historial_f2' que ahora devuelve la función
mejor_pos_f2, mejor_val_f2, historial_f2 = estrategia_evolutiva(funcion_2, limites_f2, D, miu, lamb, gen)

print("\n--- Resultados Finales funcion 2 ---")
print(f"Minimo conocido en: [0, 0] con valor 0")
print(f"Minimo encontrado en: [{mejor_pos_f2[0]:.5f}, {mejor_pos_f2[1]:.5f}] con valor {mejor_val_f2:.5f}\n")

# --- GRAFICA FUNCION 2 ---
plt.figure()
plt.plot(historial_f2, color='green')
plt.title("Convergencia para funcion 2")
plt.xlabel("Generacion")
plt.ylabel("Mejor Fitness")
plt.grid(True)
plt.show() 
# ------------------------------------
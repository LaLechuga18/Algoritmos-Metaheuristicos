import numpy as np
import math

# --- DEFINICIÓN DE LAS FUNCIONES OBJETIVO ---

def funcion_1(x):
    x0, x1 = x
    return x0 * math.exp(-(x0**2 + x1**2))

def funcion_2(x):
    x0, x1 = x
    return x0**2 + x1**2

# --- COMPONENTES DEL ALGORITMO GENÉTICO ---
def crear_individuo(limites):
    #Crea un individuo aleatorio dentro de los límites
    return [np.random.uniform(b[0], b[1]) for b in limites]

def calcular_aptitud(individuo, funcion_objetivo):
    valor_funcion = funcion_objetivo(individuo)
    return -valor_funcion

def seleccion_torneo(poblacion, aptitudes, k=3):
    # Se elige un índice aleatorio para el primer competidor
    mejor_idx = np.random.randint(0, len(poblacion))

    # Se eligen k-1 competidores más
    for _ in range(k - 1):
        idx = np.random.randint(0, len(poblacion))
        if aptitudes[idx] > aptitudes[mejor_idx]:
            mejor_idx = idx
            
    return poblacion[mejor_idx]

def cruce_aritmetico(padre1, padre2, tasa_cruce):
    #Realiza un cruce aritmético (promedio ponderado) entre dos padres.
    hijo1, hijo2 = list(padre1), list(padre2)
    if np.random.rand() < tasa_cruce:
        # Elige un peso aleatorio
        alpha = np.random.rand()
        hijo1 = [alpha * p1 + (1 - alpha) * p2 for p1, p2 in zip(padre1, padre2)]
        hijo2 = [(1 - alpha) * p1 + alpha * p2 for p1, p2 in zip(padre1, padre2)]
    return hijo1, hijo2

def mutacion_gaussiana(individuo, tasa_mutacion, limites):
    # Aplica una mutación gaussiana a un individuo con una cierta tasa de mutación.
    individuo_mutado = list(individuo)
    for i in range(len(individuo_mutado)):
        if np.random.rand() < tasa_mutacion:
            # Añade un pequeño valor aleatorio (media 0, desv. estándar 0.5)
            mutacion = np.random.normal(0, 0.5)
            individuo_mutado[i] += mutacion
            
            # Asegura que el valor mutado se mantenga dentro de los límites
            individuo_mutado[i] = max(limites[i][0], individuo_mutado[i])
            individuo_mutado[i] = min(limites[i][1], individuo_mutado[i])
            
    return individuo_mutado

# --- MOTOR PRINCIPAL DEL ALGORITMO GENÉTICO ---
def algoritmo_genetico(funcion_objetivo, limites, n_generaciones, n_poblacion, tasa_cruce, tasa_mutacion):
    # 1. Crear la población inicial
    poblacion = [crear_individuo(limites) for _ in range(n_poblacion)]
    
    mejor_solucion = None
    mejor_aptitud = -float('inf')

    print("Ejecutando Algoritmo Genético...")
    for gen in range(n_generaciones):
        # 2. Calcular la aptitud de toda la población
        aptitudes = [calcular_aptitud(ind, funcion_objetivo) for ind in poblacion]

        # Guardar la mejor solución encontrada hasta ahora
        for i in range(n_poblacion):
            if aptitudes[i] > mejor_aptitud:
                mejor_aptitud = aptitudes[i]
                mejor_solucion = poblacion[i]
        
        # Imprimir progreso cada 25 generaciones
        if (gen + 1) % 25 == 0:
            print(f"> Gen {gen+1}, Mejor Valor f(x) = {-mejor_aptitud:.5f}")

        # 3. Crear la nueva generación
        nueva_poblacion = []
        while len(nueva_poblacion) < n_poblacion:
            # Selección de padres
            padre1 = seleccion_torneo(poblacion, aptitudes)
            padre2 = seleccion_torneo(poblacion, aptitudes)
            
            # Cruce
            hijo1, hijo2 = cruce_aritmetico(padre1, padre2, tasa_cruce)
            
            # Mutación
            hijo1 = mutacion_gaussiana(hijo1, tasa_mutacion, limites)
            hijo2 = mutacion_gaussiana(hijo2, tasa_mutacion, limites)
            
            nueva_poblacion.extend([hijo1, hijo2])
        
        # Reemplazar la población antigua por la nueva
        poblacion = nueva_poblacion[:n_poblacion]

    valor_minimo = funcion_objetivo(mejor_solucion)
    return mejor_solucion, valor_minimo

# --- EJECUCIÓN DEL PROGRAMA ---

if __name__ == "__main__":
    
    # --- PARÁMETROS PARA LA FUNCIÓN 1 ---
    print("--- Problema 1: ---")
    LIMITES_F1 = [(-2, 2), (-2, 2)]
    N_GENERACIONES_F1 = 150
    N_POBLACION_F1 = 100
    TASA_CRUCE_F1 = 0.8
    TASA_MUTACION_F1 = 0.05

    mejor_sol_f1, valor_min_f1 = algoritmo_genetico(
        funcion_objetivo=funcion_1,
        limites=LIMITES_F1,
        n_generaciones=N_GENERACIONES_F1,
        n_poblacion=N_POBLACION_F1,
        tasa_cruce=TASA_CRUCE_F1,
        tasa_mutacion=TASA_MUTACION_F1
    )
    
    print("\n--- Resultados para la Función 1 ---")
    print(f"Mínimo global encontrado en: [{mejor_sol_f1[0]:.5f}, {mejor_sol_f1[1]:.5f}]")
    print(f"Valor mínimo de la función: {valor_min_f1:.5f}")
    print("-" * 40)

    # --- PARÁMETROS PARA LA FUNCIÓN 2 ---
    print("\n--- Problema 2: ---")
    LIMITES_F2 = [(-5.12, 5.12), (-5.12, 5.12)]
    N_GENERACIONES_F2 = 50
    N_POBLACION_F2 = 50
    TASA_CRUCE_F2 = 0.8
    TASA_MUTACION_F2 = 0.02
    
    mejor_sol_f2, valor_min_f2 = algoritmo_genetico(
        funcion_objetivo=funcion_2,
        limites=LIMITES_F2,
        n_generaciones=N_GENERACIONES_F2,
        n_poblacion=N_POBLACION_F2,
        tasa_cruce=TASA_CRUCE_F2,
        tasa_mutacion=TASA_MUTACION_F2
    )
    
    print("\n--- Resultados para la Función 2 ---")
    print(f"Mínimo global encontrado en: [{mejor_sol_f2[0]:.5f}, {mejor_sol_f2[1]:.5f}]")
    print(f"Valor mínimo de la función: {valor_min_f2:.5f}")
    print("-" * 40)
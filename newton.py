import numpy as np
import matplotlib.pyplot as plt

# Metodo de Newton
def newton_method(f1, f2, x0, tol=1e-6, max_iter=100):
    xi = x0
    for _ in range(max_iter):
        if f2(xi) == 0:
            break
        xiplus1 = xi - f1(xi) / f2(xi)
        if abs(xiplus1 - xi) < tol:
            return xiplus1
        xi = xiplus1
    return xi

# ======================
# Funcion 1: f(x) = sin(2x)
# ======================
def f1(x): return np.sin(2*x)
def f1_prime(x): return 2*np.cos(2*x)
def f1_second(x): return -4*np.sin(2*x)

# ======================
# Funcion 2: f(x) = sin(x) + x cos(x)
# ======================
def f2(x): return np.sin(x) + x*np.cos(x)
def f2_prime(x): return -x*np.sin(x) + 2*np.cos(x)
def f2_second(x): return -x*np.cos(x) - 3*np.sin(x)

# ======================
# Busqueda de raíces con diferentes puntos iniciales
# ======================
def encontrar_extremos(f, f1, f2, intervalo, n=20):
    guesses = np.linspace(intervalo[0], intervalo[1], n)
    criticos = []
    for g in guesses:
        root = newton_method(f1, f2, g)
        if intervalo[0] <= root <= intervalo[1]:
            root = round(root, 4)  # redondear
            if root not in [r[0] for r in criticos]:
                tipo = "minimo" if f2(root) > 0 else "maximo"
                criticos.append((root, f(root), tipo))
    return criticos

# ======================
# Ejecutar para cada función
# ======================
extremos_f1 = encontrar_extremos(f1, f1_prime, f1_second, [-4,4])
extremos_f2 = encontrar_extremos(f2, f2_prime, f2_second, [-5,5])

print("Funcion 1: f(x) = sin(2x)")
for r in extremos_f1:
    print(f"x = {r[0]}, f(x) = {round(r[1],4)}, {r[2]}")

print("\nFuncion 2: f(x) = sin(x) + x cos(x)")
for r in extremos_f2:
    print(f"x = {r[0]}, f(x) = {round(r[1],4)}, {r[2]}")

# ======================
# Graficar
# ======================
fig, axs = plt.subplots(2, 1, figsize=(8,10))

# Grafica f1
x_vals = np.linspace(-4,4,400)
axs[0].plot(x_vals, f1(x_vals), label="f(x) = sin(2x)")
for r in extremos_f1:
    color = "red" if r[2] == "máximo" else "blue"
    axs[0].scatter(r[0], r[1], c=color, s=80, label=r[2])
axs[0].set_title("Extremos de f(x) = sin(2x)")
axs[0].grid(True)
axs[0].legend()

# Grafica f2
x_vals = np.linspace(-5,5,400)
axs[1].plot(x_vals, f2(x_vals), label="f(x) = sin(x) + x cos(x)")
for r in extremos_f2:
    color = "red" if r[2] == "máximo" else "blue"
    axs[1].scatter(r[0], r[1], c=color, s=80, label=r[2])
axs[1].set_title("Extremos de f(x) = sin(x) + x cos(x)")
axs[1].grid(True)
axs[1].legend()

plt.tight_layout()
plt.show()

from itertools import product
from math import ceil

def calcular_conflicto(rs, estrategia):
    numerador = sum(
        (grupo[0] - estrategia[i]) * (grupo[1] - grupo[2]) ** 2
        for i, grupo in enumerate(rs)
    )
    denominador = sum(grupo[0] - estrategia[i] for i, grupo in enumerate(rs))
    return numerador / denominador if denominador > 0 else 0

def calcular_esfuerzo(rs, estrategia):
    return sum(
        ceil(abs(grupo[1] - grupo[2]) * grupo[3] * estrategia[i])
        for i, grupo in enumerate(rs)
    )

def modci_fuerza_bruta(rs, r_max):
    n = len(rs)
    todas_estrategias = []
    
    for estrategia in product(*(range(grupo[0] + 1) for grupo in rs)):
        esfuerzo = calcular_esfuerzo(rs, estrategia)
        conflicto = calcular_conflicto(rs, estrategia)
        todas_estrategias.append((estrategia, esfuerzo, conflicto))
    
    return todas_estrategias

# Ejemplo de uso con los datos del documento
data = [
    (3, -100, 100, 0.8),
    (2, 100, 80, 0.5),
    (4, -10, 10, 0.5)
]
r_max = 400

estrategias = modci_fuerza_bruta(data, r_max)
for estrategia, esfuerzo, conflicto in estrategias:
    print("Estrategia:", estrategia, "Esfuerzo:", esfuerzo, "Conflicto interno:", conflicto)

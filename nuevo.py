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
    mejores_estrategia = None
    menor_conflicto = float('inf')
    mejor_esfuerzo = float('inf')
    
    for estrategia in product(*(range(grupo[0] + 1) for grupo in rs)):
        esfuerzo = calcular_esfuerzo(rs, estrategia)
        if esfuerzo <= r_max:
            conflicto = calcular_conflicto(rs, estrategia)
            if conflicto < menor_conflicto:
                menor_conflicto = conflicto
                mejores_estrategia = estrategia
                mejor_esfuerzo = esfuerzo
    
    return mejores_estrategia, mejor_esfuerzo, menor_conflicto

# Ejemplo de uso con los datos del documento
data = [
    (3, -100, 50, 0.5),
    (1, 100, 80, 0.1),
    (1, -10, 0, 0.5)
]
r_max = 80

estrategia, esfuerzo, conflicto = modci_fuerza_bruta(data, r_max)
print("Mejor estrategia:", estrategia)
print("Esfuerzo:", esfuerzo)
print("Conflicto interno:", conflicto)


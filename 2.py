import math

#  n_i: Número de agentes en un grupo.
# o_i1 y o_i2: Opiniones extremas dentro del grupo.
# r_i: Un factor de resistencia al cambio de opinión.


# Función para calcular el esfuerzo
def esfuerzo_modificacion(RS, estrategia):
    esfuerzo = 0
    for i, (n_i, o_i1, o_i2, r_i) in enumerate(RS):
        e_i = estrategia[i]
        if e_i > 0:
            # Cálculo del esfuerzo con el valor absoluto de la diferencia de opiniones
            esfuerzo += math.ceil(abs(o_i1 - o_i2) * r_i * e_i)
    return esfuerzo



# Función para calcular el conflicto interno
def calcular_conflicto_interno(RS):
    numerador = 0
    denominador = 0
    for n_i, o_i1, o_i2, r_i in RS:
        numerador += n_i * (o_i1 - o_i2) ** 2
        denominador += n_i
    return numerador / denominador if denominador != 0 else 0

# Red RS2
RS2 = [
    (3, -100, 100, 0.8),  # (n_i, o_i1, o_i2, r_i)
    (2, 100, 80, 0.5),
    (4, -10, 10, 0.5)
]

# Estrategia E1
estrategia = [2, 2, 2]  # Cambia 0 agentes en el primer grupo, 1 en el segundo, y 1 en el tercero

# Calculamos el esfuerzo
esfuerzo = esfuerzo_modificacion(RS2, estrategia)

# Aplicamos la estrategia para modificar la red
RS_modificada = [(n_i - e_i, o_i1, o_i2, r_i) for (n_i, o_i1, o_i2, r_i), e_i in zip(RS2, estrategia)]

# Calculamos el conflicto interno
conflicto_interno_modificado = calcular_conflicto_interno(RS_modificada)

# Mostrar los resultados
print(f"Esfuerzo de la Estrategia: {esfuerzo}")
print(f"Conflicto Interno Modificado: {conflicto_interno_modificado}")

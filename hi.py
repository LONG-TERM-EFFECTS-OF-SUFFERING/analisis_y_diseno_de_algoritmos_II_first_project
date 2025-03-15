import math

def calcular_conflicto_interno(RS):
    """
    Calcula el conflicto interno de una red social RS.
    
    Parámetros:
    RS (list): Red social en formato [(n_i, o_i1, o_i2, r_i), ...]
    
    Retorna:
    float: El valor del conflicto interno CI(RS).
    """
    numerador = 0
    denominador = 0
    
    for n_i, o_i1, o_i2, r_i in RS:
        # Calculamos el conflicto para el grupo de agentes i
        numerador += n_i * (o_i1 - o_i2) ** 2
        denominador += n_i
    
    # El conflicto interno es el numerador dividido por el denominador
    return numerador / denominador if denominador != 0 else 0

def aplicar_estrategia_modificacion(RS, estrategia):
    """
    Aplica una estrategia de cambio de opinión a la red RS, obteniendo la nueva red RS'.
    
    Parámetros:
    RS (list): Red social en formato [(n_i, o_i1, o_i2, r_i), ...]
    estrategia (list): Estrategia de cambio de opinión que indica cuántos agentes deben cambiar su opinión en cada grupo.
    
    Retorna:
    list: Nueva red RS' con los agentes cuya opinión ha sido cambiada eliminados.
    """
    RS_modificada = []

    for i, (n_i, o_i1, o_i2, r_i) in enumerate(RS):
        e_i = estrategia[i]  # Estrategia de cambio para el grupo i

        # Calculamos el nuevo número de agentes en el grupo i después de aplicar la estrategia
        if e_i > 0:
            n_i_modificada = n_i - e_i  # Los agentes cuyo opinión ha sido cambiada ya no participan
        else:
            n_i_modificada = n_i  # No se cambian agentes, el grupo queda igual

        # Solo agregamos al grupo modificado si tiene agentes restantes
        if n_i_modificada > 0:
            RS_modificada.append((n_i_modificada, o_i1, o_i2, r_i))

    return RS_modificada

def esfuerzo_modificacion(RS, estrategia):
    """
    Calcula el esfuerzo de aplicar una estrategia de cambio de opinión en la red RS.
    
    Parámetros:
    RS (list): Red social en formato [(n_i, o_i1, o_i2, r_i), ...]
    estrategia (list): Estrategia de cambio de opinión que indica cuántos agentes deben cambiar su opinión en cada grupo.
    
    Retorna:
    int: El esfuerzo total de la estrategia.
    """
    esfuerzo = 0
    for i, (n_i, o_i1, o_i2, r_i) in enumerate(RS):
        e_i = estrategia[i]  # Estrategia de cambio para el grupo i
        if e_i > 0:
            esfuerzo += math.ceil(abs(o_i1 - o_i2) * r_i * e_i)
    
    return esfuerzo

# Ejemplo de uso:

# Red original RS1: [(n_i, o_i1, o_i2, r_i)]
RS1 = [
    (3, -100, 100, 0.8),  # (n_i, o_i1, o_i2, r_i)
    (2, 100, 80, 0.5),
    (4, -10, 10, 0.5)
]

# Estrategia de cambio de opinión, cambia 1 agente en el grupo 1 y 2
estrategia = [1, 0, 0]  


# Aplicamos la estrategia de cambio de opinión
RS_modificada = aplicar_estrategia_modificacion(RS1, estrategia)

# Calculamos el esfuerzo de la estrategia
esfuerzo = esfuerzo_modificacion(RS1, estrategia)

# Calculamos el conflicto interno de la red original
conflicto_interno_original = calcular_conflicto_interno(RS1)

# Calculamos el conflicto interno de la nueva red después de aplicar la estrategia
conflicto_interno_modificado = calcular_conflicto_interno(RS_modificada)

# Mostramos los resultados
print(f"Conflicto Interno Original: {conflicto_interno_original}")
print(f"Conflicto Interno Modificado: {conflicto_interno_modificado}")
print(f"Esfuerzo de la Estrategia: {esfuerzo}")

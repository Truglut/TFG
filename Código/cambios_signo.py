def signo(f):
    if f > 0:
        return 1
    if f < 0:
        return -1
    if f == 0:
        return 0

def cambios_signo(l):
    """
    Calcula el número de cambios de signo en la lista de números l, de acuerdo
    con la definición para la secuencia de Sturm.
    """

    i = 0
    j = 1
    k = len(l)
    cambios = 0
    while i < k - 1:
        if l[i] == 0:
            i += 1
            continue
        while j < k and l[j] == 0:
            j += 1
        
        if j == k:
            break

        if signo(l[i]) != signo(l[j]):
            cambios += 1
        
        i = j
        j = i + 1
    
    return cambios

def ningun_cambio(l):
    return all(signo(r) >= 0 for r in l) or all(signo(r) <= 0 for r in l)
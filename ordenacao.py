"""Ordenação rápida (quicksort) pura e híbrida com inserção.

As três funções devolvem a lista ordenada sem alterar a lista recebida.

Autores: Samuel Ribeiro Cardoso e Pedro Augusto
"""

import random


def insercao(v):
    """Ordenação por inserção: O(n²) no pior caso, mas muito barata em listas pequenas."""
    a = list(v)
    for i in range(1, len(a)):
        chave = a[i]
        j = i - 1
        while j >= 0 and a[j] > chave:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = chave
    return a


def quicksort(v):
    """Rápida pura: pivô aleatório, partição em menores, iguais e maiores."""
    if len(v) <= 1:
        return v
    pivo = random.choice(v)
    menores = [x for x in v if x < pivo]
    iguais = [x for x in v if x == pivo]
    maiores = [x for x in v if x > pivo]
    return quicksort(menores) + iguais + quicksort(maiores)


def quicksort_hibrido(v, corte):
    """Rápida que entrega à inserção todo pedaço com menos de `corte` elementos.

    O caso base é o mesmo da pura (len <= 1). Assim, com corte = 1 a condição
    `len(v) < 1` nunca é atingida e a função faz exatamente o que a pura faz.
    """
    if len(v) <= 1:
        return v
    if len(v) < corte:
        return insercao(v)
    pivo = random.choice(v)
    menores = [x for x in v if x < pivo]
    iguais = [x for x in v if x == pivo]
    maiores = [x for x in v if x > pivo]
    return quicksort_hibrido(menores, corte) + iguais + quicksort_hibrido(maiores, corte)

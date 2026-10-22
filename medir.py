"""Mede o tempo da rápida pura e da híbrida variando o corte.

Gera `resultados.csv` (um resumo por variante) e imprime a tabela em Markdown.
Rodar com: python medir.py

Autores: Samuel Ribeiro Cardoso e Pedro Augusto
"""

import csv
import gc
import random
import statistics
import time

import ordenacao

N = 20_000
CORTES = [1, 5, 10, 16, 20, 32, 50, 100, 200]
REPETICOES = 50
SEMENTE = 2026

# (nome, corte); corte None = rápida pura
VARIANTES = [("pura", None)] + [("hibrida", c) for c in CORTES]


def ordenar(v, corte):
    if corte is None:
        return ordenacao.quicksort(v)
    return ordenacao.quicksort_hibrido(v, corte)


def cronometrar(v, corte):
    """Tempo de uma ordenação, em ms, com o coletor de lixo desligado."""
    gc.collect()
    gc.disable()
    try:
        inicio = time.perf_counter()
        resultado = ordenar(v, corte)
        fim = time.perf_counter()
    finally:
        gc.enable()
    return (fim - inicio) * 1000, resultado


def contar_chamadas(v, corte, semente):
    """Quantas vezes a rápida e a inserção são chamadas para ordenar `v`.

    Troca temporariamente as funções do módulo por versões que contam; como a
    recursão procura o nome no módulo, as chamadas recursivas também são contadas.
    """
    contagem = {"rapida": 0, "insercao": 0}
    originais = {
        "quicksort": ordenacao.quicksort,
        "quicksort_hibrido": ordenacao.quicksort_hibrido,
        "insercao": ordenacao.insercao,
    }

    def contando(chave, funcao):
        def envoltorio(*args):
            contagem[chave] += 1
            return funcao(*args)
        return envoltorio

    ordenacao.quicksort = contando("rapida", originais["quicksort"])
    ordenacao.quicksort_hibrido = contando("rapida", originais["quicksort_hibrido"])
    ordenacao.insercao = contando("insercao", originais["insercao"])
    try:
        random.seed(semente)
        ordenar(v, corte)
    finally:
        for nome, funcao in originais.items():
            setattr(ordenacao, nome, funcao)
    return contagem


def main():
    random.seed(SEMENTE)
    tempos = {variante: [] for variante in VARIANTES}

    for rep in range(REPETICOES):
        v = [random.randint(0, 1_000_000) for _ in range(N)]
        esperado = sorted(v)
        # Mesma lista para todas as variantes, em ordem sorteada a cada
        # repetição, para nenhum corte levar vantagem por rodar sempre antes.
        ordem = VARIANTES[:]
        random.shuffle(ordem)
        for variante in ordem:
            ms, resultado = cronometrar(v, variante[1])
            assert resultado == esperado, f"{variante} ordenou errado"
            tempos[variante].append(ms)
        print(f"repetição {rep + 1}/{REPETICOES}", end="\r", flush=True)
    print()

    # Contagem de chamadas numa lista fixa, com a mesma semente para todos.
    gerador = random.Random(7)
    lista_fixa = [gerador.randint(0, 1_000_000) for _ in range(N)]
    chamadas = {variante: contar_chamadas(lista_fixa, variante[1], semente=99)
                for variante in VARIANTES}

    pura = statistics.median(tempos[("pura", None)])
    linhas = []
    for nome, corte in VARIANTES:
        amostra = tempos[(nome, corte)]
        q1, _, q3 = statistics.quantiles(amostra, n=4)
        mediana = statistics.median(amostra)
        linhas.append({
            "variante": nome,
            "corte": "" if corte is None else corte,
            "mediana_ms": round(mediana, 3),
            "q1_ms": round(q1, 3),
            "q3_ms": round(q3, 3),
            "min_ms": round(min(amostra), 3),
            "ganho_sobre_pura_pct": round((pura - mediana) / pura * 100, 1),
            "chamadas_rapida": chamadas[(nome, corte)]["rapida"],
            "chamadas_insercao": chamadas[(nome, corte)]["insercao"],
        })

    with open("resultados.csv", "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=linhas[0].keys())
        escritor.writeheader()
        escritor.writerows(linhas)

    print(f"n = {N}, {REPETICOES} repetições, mediana em ms\n")
    print("| Variante | Corte | Mediana (ms) | Q1–Q3 (ms) | Ganho sobre a pura "
          "| Chamadas da rápida | Chamadas da inserção |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    for l in linhas:
        variante = "rápida pura" if l["variante"] == "pura" else "híbrida"
        corte = l["corte"] if l["corte"] != "" else "—"
        print(f"| {variante} | {corte} | {l['mediana_ms']:.1f} "
              f"| {l['q1_ms']:.1f}–{l['q3_ms']:.1f} | {l['ganho_sobre_pura_pct']:+.1f}% "
              f"| {l['chamadas_rapida']:,} | {l['chamadas_insercao']:,} |")


if __name__ == "__main__":
    main()

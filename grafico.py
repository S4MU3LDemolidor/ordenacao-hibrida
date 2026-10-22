"""Gráfico do tempo da híbrida em função do corte, a partir de `resultados.csv`.

Rodar depois de `medir.py`: python grafico.py  ->  grafico_corte.png

Autores: Samuel Ribeiro Cardoso e Pedro Augusto
"""

import csv

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, NullLocator

SUPERFICIE = "#fcfcfb"
TEXTO = "#0b0b0b"
TEXTO_2 = "#52514e"
GRADE = "#e4e3df"
SERIE = "#2a78d6"


def virgula(x, casas=1):
    return f"{x:.{casas}f}".replace(".", ",")


def ler():
    with open("resultados.csv", encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    pura = next(l for l in linhas if l["variante"] == "pura")
    hibrida = [l for l in linhas if l["variante"] == "hibrida"]
    return pura, hibrida


def main():
    pura, hibrida = ler()
    cortes = [int(l["corte"]) for l in hibrida]
    mediana = [float(l["mediana_ms"]) for l in hibrida]
    q1 = [float(l["q1_ms"]) for l in hibrida]
    q3 = [float(l["q3_ms"]) for l in hibrida]
    t_pura = float(pura["mediana_ms"])
    i_melhor = min(range(len(mediana)), key=mediana.__getitem__)

    plt.rcParams.update({"font.size": 10, "text.color": TEXTO, "axes.labelcolor": TEXTO_2,
                         "xtick.color": TEXTO_2, "ytick.color": TEXTO_2})
    fig, ax = plt.subplots(figsize=(8, 4.6), dpi=200)
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    # Referência: rápida pura
    ax.axhline(t_pura, color=TEXTO_2, lw=1.2, ls=(0, (5, 4)), zorder=1)
    ax.text(1.6, t_pura + 0.35, f"rápida pura · {virgula(t_pura)} ms",
            ha="left", va="bottom", color=TEXTO_2, fontsize=9)

    # Híbrida: faixa interquartil + mediana
    ax.fill_between(cortes, q1, q3, color=SERIE, alpha=0.15, lw=0, zorder=2)
    ax.plot(cortes, mediana, color=SERIE, lw=2, zorder=3,
            marker="o", ms=7, mfc=SERIE, mec=SUPERFICIE, mew=1.5)

    # Rótulos seletivos: melhor corte e corte = 1
    c, t = cortes[i_melhor], mediana[i_melhor]
    ganho = (t_pura - t) / t_pura * 100
    ax.annotate(f"melhor: corte {c}\n{virgula(t)} ms ({virgula(ganho)}% mais rápida)",
                xy=(c, t), xytext=(c, t - 3.2), ha="center", va="top", fontsize=9,
                color=TEXTO, arrowprops=dict(arrowstyle="-", color=TEXTO_2, lw=0.8))
    ax.annotate("corte 1 = rápida pura", xy=(cortes[0], mediana[0]),
                xytext=(cortes[0] * 1.15, mediana[0] - 2.6), ha="left", va="top",
                fontsize=9, color=TEXTO,
                arrowprops=dict(arrowstyle="-", color=TEXTO_2, lw=0.8))
    ax.annotate(f"corte 200: {virgula(mediana[-1])} ms", xy=(cortes[-1], mediana[-1]),
                xytext=(-10, 0), textcoords="offset points", ha="right", va="center",
                fontsize=9, color=TEXTO)

    # Eixos
    ax.set_xscale("log")
    ax.xaxis.set_major_locator(FixedLocator(cortes))
    ax.xaxis.set_minor_locator(NullLocator())
    ax.set_xticklabels([str(c) for c in cortes])
    ax.set_xlim(0.8, 250)
    ax.set_ylim(0, 20)
    ax.set_yticks(range(0, 21, 5))
    ax.set_xlabel("corte (escala logarítmica): pedaços com menos elementos vão para a inserção")
    ax.set_ylabel("tempo mediano (ms)")
    ax.grid(axis="y", color=GRADE, lw=0.8)
    ax.set_axisbelow(True)
    for lado in ("top", "right", "left"):
        ax.spines[lado].set_visible(False)
    ax.spines["bottom"].set_color(GRADE)
    ax.tick_params(length=0, pad=6)

    fig.text(0.015, 0.97, "Tempo da ordenação híbrida em função do corte",
             fontsize=13, fontweight="bold", color=TEXTO, va="top")
    fig.text(0.015, 0.905, "20 000 inteiros aleatórios · mediana de 50 repetições · "
             "faixa sombreada = 1º ao 3º quartil", fontsize=9, color=TEXTO_2, va="top")
    fig.subplots_adjust(left=0.08, right=0.98, top=0.82, bottom=0.13)
    fig.savefig("grafico_corte.png", facecolor=SUPERFICIE)
    print("grafico_corte.png gerado")


if __name__ == "__main__":
    main()

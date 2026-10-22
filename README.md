# Ordenação híbrida: rápida + inserção

**Dupla:** Samuel Ribeiro Cardoso e Pedro Augusto

Ordenação rápida (quicksort) com pivô aleatório e partição em menores, iguais e maiores, que entrega à ordenação por inserção todo pedaço com menos de `corte` elementos. Medimos o tempo com 20 mil elementos aleatórios para os cortes 1, 5, 10, 16, 20, 32, 50, 100 e 200 e comparamos com a rápida pura.

Resultados, gráfico e análise: **[RELATORIO.md](RELATORIO.md)**.

![Tempo em função do corte](grafico_corte.png)

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `ordenacao.py` | `insercao`, `quicksort` (pura) e `quicksort_hibrido(v, corte)` |
| `medir.py` | medição dos tempos → `resultados.csv` |
| `grafico.py` | gráfico do tempo em função do corte → `grafico_corte.png` |
| `test_ordenacao.py` | testes de correção |
| `RELATORIO.md` | tabela, gráfico e conclusões |

## Como rodar

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m unittest -v
.venv/bin/python medir.py
.venv/bin/python grafico.py
```

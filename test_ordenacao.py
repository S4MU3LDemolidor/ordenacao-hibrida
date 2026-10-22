"""Testes de correção das ordenações. Rodar com: python -m unittest -v

Autores: Samuel Ribeiro Cardoso e Pedro Augusto
"""

import random
import unittest

from ordenacao import insercao, quicksort, quicksort_hibrido

CORTES = [1, 2, 5, 10, 16, 20, 32, 50, 100, 200]


def casos():
    rnd = random.Random(42)
    return {
        "vazia": [],
        "um elemento": [7],
        "dois elementos": [2, 1],
        "ja ordenada": list(range(300)),
        "invertida": list(range(300, 0, -1)),
        "todos iguais": [5] * 300,
        "muitos repetidos": [rnd.randint(0, 3) for _ in range(500)],
        "aleatoria": [rnd.randint(-10_000, 10_000) for _ in range(2_000)],
    }


class TestInsercao(unittest.TestCase):
    def test_ordena(self):
        for nome, v in casos().items():
            with self.subTest(caso=nome):
                self.assertEqual(insercao(v), sorted(v))

    def test_nao_altera_a_entrada(self):
        v = [3, 1, 2]
        insercao(v)
        self.assertEqual(v, [3, 1, 2])


class TestQuicksort(unittest.TestCase):
    def test_ordena(self):
        for nome, v in casos().items():
            with self.subTest(caso=nome):
                self.assertEqual(quicksort(v), sorted(v))

    def test_nao_altera_a_entrada(self):
        v = [3, 1, 2]
        quicksort(v)
        self.assertEqual(v, [3, 1, 2])


class TestQuicksortHibrido(unittest.TestCase):
    def test_ordena_com_qualquer_corte(self):
        for corte in CORTES + [10_000]:
            for nome, v in casos().items():
                with self.subTest(corte=corte, caso=nome):
                    self.assertEqual(quicksort_hibrido(v, corte), sorted(v))

    def test_nao_altera_a_entrada(self):
        v = [3, 1, 2]
        quicksort_hibrido(v, corte=10)  # pedaço inteiro vai para a inserção
        self.assertEqual(v, [3, 1, 2])

    def test_corte_1_faz_as_mesmas_escolhas_que_a_pura(self):
        # Com a mesma semente, os pivôs sorteados só coincidem se as duas
        # funções fizerem exatamente as mesmas chamadas, na mesma ordem.
        v = [random.Random(1).randint(0, 1000) for _ in range(1_000)]
        random.seed(123)
        quicksort(v)
        proximo_pura = random.random()
        random.seed(123)
        quicksort_hibrido(v, corte=1)
        proximo_hibrido = random.random()
        self.assertEqual(proximo_pura, proximo_hibrido)


if __name__ == "__main__":
    unittest.main()

"""Verificação de corretude: Alfa-Beta deve devolver EXATAMENTE o valor do Minimax.

Teste 1: profundidade completa em tabuleiros pequenos e em posições finais do 6x7.
Teste 2: profundidade limitada (usa a avaliação) em posições do 6x7.
Mostra também quantos nós cada um visitou.
"""
import random
from jogo import Jogo
from busca import minimax, alfabeta, INF

rng = random.Random(42)


def posicao_aleatoria(L, C, K, n_jogadas):
    """Joga n_jogadas aleatórias (se o jogo acabar antes, tenta de novo)."""
    while True:
        j = Jogo(L, C, K)
        for _ in range(n_jogadas):
            if j.terminal():
                break
            j.jogar(rng.choice(j.acoes()))
        if not j.terminal():
            return j


def comparar(jogo, d):
    meu = jogo.vez                        # MAX = quem joga agora
    c1, c2 = [0], [0]
    v_mm = minimax(jogo, d, meu, c1)
    v_ab = alfabeta(jogo, d, -INF, INF, meu, c2)
    return v_mm, v_ab, c1[0], c2[0]


def rodar(titulo, casos):
    print(f"\n{titulo}")
    print(f"{'caso':<24}{'Minimax':>10}{'AlfaBeta':>10}{'nós MM':>12}{'nós AB':>10}  igual?")
    todos_iguais = True
    for nome, jogo, d in casos:
        v1, v2, n1, n2 = comparar(jogo, d)
        igual = v1 == v2
        todos_iguais &= igual
        print(f"{nome:<24}{v1:>10}{v2:>10}{n1:>12}{n2:>10}  {'OK' if igual else 'DIFERENTE!'}")
    return todos_iguais


if __name__ == "__main__":
    ok = True

    # Teste 1a: tabuleiros pequenos, tabuleiro vazio, profundidade completa
    casos = []
    for L, C, K in [(3, 3, 3), (3, 4, 3), (4, 4, 3)]:
        casos.append((f"{L}x{C} k={K} vazio", Jogo(L, C, K), L * C))
    ok &= rodar("TESTE 1a - profundidade completa, tabuleiros pequenos", casos)

    # Teste 1b: 6x7 k=4, posições com poucas casas vazias (profundidade completa)
    casos = [(f"6x7 faltam 14 (#{i+1})", posicao_aleatoria(6, 7, 4, 28), 42) for i in range(5)]
    ok &= rodar("TESTE 1b - profundidade completa, 6x7 quase cheio", casos)

    # Teste 2: 6x7 em posições aleatórias, profundidade limitada (com heurística)
    casos = []
    for i in range(10):
        casos.append((f"6x7 meio-jogo #{i+1} d=4", posicao_aleatoria(6, 7, 4, rng.randint(4, 20)), 4))
    ok &= rodar("TESTE 2 - profundidade limitada (com avaliação), 6x7", casos)

    print("\nRESULTADO FINAL:", "TODOS OS VALORES IGUAIS" if ok else "HÁ DIFERENÇAS - alfa-beta com erro!")

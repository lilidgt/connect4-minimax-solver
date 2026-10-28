"""Minimax, Alfa-Beta, função de avaliação e agentes.

Unidade de custo: NÓS VISITADOS = número de chamadas à função de busca.
O contador é uma lista de um elemento (cont[0]) passada pelas chamadas.
Todas as funções avaliam do ponto de vista do jogador `meu` (1 = X, 2 = O):
se `meu` = X, é exatamente o MAX/MIN da ficha.
"""
import random

VITORIA = 100000
INF = float("inf")


# ---------------------------------------------------------------- avaliação
def valor_terminal(jogo, meu, d):
    """Vitória +100000, derrota -100000, empate 0.
    Somamos d (profundidade que sobrou) para preferir vitórias rápidas
    e derrotas demoradas."""
    if jogo.vencedor == 0:
        return 0
    return VITORIA + d if jogo.vencedor == meu else -(VITORIA + d)


def avaliar(jogo, meu):
    """Heurística da ficha, do ponto de vista de `meu`:
    +3 por peça minha na coluna central; janela com k-1 minhas e 1 vazia +5;
    k-2 minhas e 2 vazias +2; janela com k-1 do adversário e 1 vazia -4."""
    tab, K = jogo.tab, jogo.K
    adv = 3 - meu
    centro = jogo.C // 2
    pontos = 3 * sum(1 for r in range(jogo.L) if tab[r * jogo.C + centro] == meu)
    for janela in jogo.janelas:
        n_meu = n_adv = 0
        for i in janela:
            p = tab[i]
            if p == meu:
                n_meu += 1
            elif p == adv:
                n_adv += 1
        if n_adv == 0:
            if n_meu == K - 1:
                pontos += 5
            elif n_meu == K - 2:
                pontos += 2
        elif n_meu == 0 and n_adv == K - 1:
            pontos -= 4
    return pontos


# ------------------------------------------------------------------ Minimax
def minimax(jogo, d, meu, cont):
    cont[0] += 1
    if jogo.terminal():
        return valor_terminal(jogo, meu, d)
    if d == 0:
        return avaliar(jogo, meu)
    maximiza = (jogo.vez == meu)
    melhor = -INF if maximiza else INF
    for c in jogo.acoes():
        jogo.jogar(c)
        v = minimax(jogo, d - 1, meu, cont)
        jogo.desfazer(c)
        melhor = max(melhor, v) if maximiza else min(melhor, v)
    return melhor


# --------------------------------------------------------------- Alfa-Beta
def alfabeta(jogo, d, alfa, beta, meu, cont):
    cont[0] += 1
    if jogo.terminal():
        return valor_terminal(jogo, meu, d)
    if d == 0:
        return avaliar(jogo, meu)
    maximiza = (jogo.vez == meu)
    melhor = -INF if maximiza else INF
    for c in jogo.acoes():
        jogo.jogar(c)
        v = alfabeta(jogo, d - 1, alfa, beta, meu, cont)
        jogo.desfazer(c)
        if maximiza:
            melhor = max(melhor, v)
            alfa = max(alfa, melhor)
        else:
            melhor = min(melhor, v)
            beta = min(beta, melhor)
        if alfa >= beta:      # poda
            break
    return melhor


# ------------------------------------------------------------------ Agentes
# Todo agente é uma função  agente(jogo) -> (coluna, nós_visitados)

def criar_agente_alfabeta(profundidade):
    def agente(jogo):
        meu = jogo.vez
        cont = [1]                       # conta o nó raiz
        melhor_v, melhor_c, alfa = -INF, None, -INF
        for c in jogo.acoes():
            jogo.jogar(c)
            v = alfabeta(jogo, profundidade - 1, alfa, INF, meu, cont)
            jogo.desfazer(c)
            if v > melhor_v:             # empate: fica a primeira (mais central)
                melhor_v, melhor_c = v, c
            alfa = max(alfa, melhor_v)
        return melhor_c, cont[0]
    return agente


def criar_agente_aleatorio(semente):
    rng = random.Random(semente)
    def agente(jogo):
        return rng.choice(jogo.acoes()), 0   # não faz busca: custo 0 nós
    return agente

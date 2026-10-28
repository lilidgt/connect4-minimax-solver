import random

VITORIA = 100000
INF = float("inf")


def valor_terminal(jogo, meu, d):
    # d é a profundidade que sobrou: vitória rápida vale mais, derrota rápida vale menos
    if jogo.vencedor == 0:
        return 0
    if jogo.vencedor == meu:# "meu" é o jogador que está decidindo (1 = X, 2 = O).
        return VITORIA + d
    return -(VITORIA + d)


def avaliar(jogo, meu):
    tab, K = jogo.tab, jogo.K
    adv = 3 - meu
    centro = jogo.C // 2

    # +3 por peça minha na coluna do meio
    pontos = 3 * sum(1 for r in range(jogo.L) if tab[r * jogo.C + centro] == meu)

    for janela in jogo.janelas:
        n_meu = 0
        n_adv = 0
        for i in janela:
            if tab[i] == meu:
                n_meu += 1
            elif tab[i] == adv:
                n_adv += 1
        if n_adv == 0:
            if n_meu == K - 1:
                pontos += 5
            elif n_meu == K - 2:
                pontos += 2
        elif n_meu == 0 and n_adv == K - 1:
            pontos -= 4
    return pontos


def minimax(jogo, d, meu, cont):
    cont[0] += 1
    if jogo.terminal():
        return valor_terminal(jogo, meu, d)
    if d == 0:
        return avaliar(jogo, meu)

    maximiza = jogo.vez == meu
    melhor = -INF if maximiza else INF
    for c in jogo.acoes():
        jogo.jogar(c)
        v = minimax(jogo, d - 1, meu, cont)
        jogo.desfazer(c)
        if maximiza:
            melhor = max(melhor, v)
        else:
            melhor = min(melhor, v)
    return melhor


def alfabeta(jogo, d, alfa, beta, meu, cont):
    cont[0] += 1
    if jogo.terminal():
        return valor_terminal(jogo, meu, d)
    if d == 0:
        return avaliar(jogo, meu)

    maximiza = jogo.vez == meu
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
        if alfa >= beta:   # poda
            break
    return melhor


# Cada agente recebe o jogo e devolve (coluna, nós visitados)

def criar_agente_alfabeta(profundidade):
    def agente(jogo):
        meu = jogo.vez
        cont = [1]   # já conta a raiz
        melhor_v = -INF
        melhor_c = None
        alfa = -INF
        for c in jogo.acoes():
            jogo.jogar(c)
            v = alfabeta(jogo, profundidade - 1, alfa, INF, meu, cont)
            jogo.desfazer(c)
            if v > melhor_v:   # em empate fica a primeira (a mais central)
                melhor_v = v
                melhor_c = c
            alfa = max(alfa, melhor_v)
        return melhor_c, cont[0]
    return agente


def criar_agente_aleatorio(semente):
    rng = random.Random(semente)

    def agente(jogo):
        return rng.choice(jogo.acoes()), 0   # não faz busca, custo 0
    return agente
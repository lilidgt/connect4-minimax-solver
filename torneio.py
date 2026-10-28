"""Torneio: roda os confrontos do protocolo e imprime a tabela de resultados.

Protocolo (ver ficha):
- unidade de custo: nós visitados (agente aleatório não faz busca = 0 nós)
- 50 aberturas distintas sorteadas com semente 42; cada abertura é jogada
  duas vezes: principal como X (começa) e principal como O (adversário começa)
  => 100 partidas por confronto
- abertura = 4 jogadas aleatórias (2 de cada lado), para haver 50 distintas
"""
import random
import statistics
import csv
from jogo import Jogo
from busca import criar_agente_alfabeta, criar_agente_aleatorio

SEMENTE = 42
N_ABERTURAS = 50
PLIES_ABERTURA = 4


def gerar_aberturas(n, plies, semente):
    rng = random.Random(semente)
    aberturas = set()
    while len(aberturas) < n:
        j = Jogo()
        seq = []
        for _ in range(plies):
            c = rng.choice(j.acoes())
            seq.append(c)
            j.jogar(c)
        aberturas.add(tuple(seq))
    return sorted(aberturas)          # ordem fixa => reprodutível


def partida(abertura, agente_x, agente_o):
    """Joga uma partida. Retorna (vencedor, nós_de_X, nós_de_O, n_jogadas_dos_agentes)."""
    j = Jogo()
    for c in abertura:                 # abertura sorteada (não conta custo)
        j.jogar(c)
    nos = {1: [], 2: []}               # nós por jogada de cada lado
    agentes = {1: agente_x, 2: agente_o}
    while not j.terminal():
        c, n = agentes[j.vez](j)
        nos[j.vez].append(n)
        j.jogar(c)
    return j.vencedor, nos[1], nos[2]


def confronto(nome, fab_principal, fab_adversario, aberturas):
    """Roda 2 partidas por abertura. Retorna lista de dicionários (uma linha por partida)."""
    principal, adversario = fab_principal(), fab_adversario()   # agentes novos por confronto
    linhas = []
    for ab in aberturas:
        for principal_e_x in (True, False):
            ax, ao = (principal, adversario) if principal_e_x else (adversario, principal)
            venc, nos_x, nos_o = partida(ab, ax, ao)
            meu = 1 if principal_e_x else 2
            res = "V" if venc == meu else ("E" if venc == 0 else "D")
            nos_p, nos_a = (nos_x, nos_o) if principal_e_x else (nos_o, nos_x)
            linhas.append(dict(confronto=nome, abertura="".join(map(str, ab)),
                               principal_comeca=principal_e_x, resultado=res,
                               jogadas=len(nos_x) + len(nos_o),
                               nos_principal=sum(nos_p), nos_adversario=sum(nos_a),
                               max_nos_jogada_principal=max(nos_p),
                               max_nos_jogada_adversario=max(nos_a)))
    return linhas


def resumo(nome, linhas):
    n = len(linhas)
    def taxa(res, filtro=lambda l: True):
        sub = [l for l in linhas if filtro(l)]
        return sum(l["resultado"] == res for l in sub), len(sub)
    print(f"\n=== {nome} ({n} partidas) ===")
    for rotulo, filtro in [("total", lambda l: True),
                           ("principal começa", lambda l: l["principal_comeca"]),
                           ("adversário começa", lambda l: not l["principal_comeca"])]:
        v, t = taxa("V", filtro); e, _ = taxa("E", filtro); d, _ = taxa("D", filtro)
        print(f"  {rotulo:<18} V={v:>3} E={e:>3} D={d:>3}   (vitórias {100*v/t:.0f}%)")
    print(f"  {'custo (nós)':<28}{'média':>12}{'mediana':>12}{'pior caso':>12}")
    for rotulo, chave in [("principal, por partida", "nos_principal"),
                          ("adversário, por partida", "nos_adversario"),
                          ("principal, pior jogada", "max_nos_jogada_principal"),
                          ("adversário, pior jogada", "max_nos_jogada_adversario")]:
        xs = [l[chave] for l in linhas]
        print(f"  {rotulo:<28}{statistics.mean(xs):>12.0f}{statistics.median(xs):>12.0f}{max(xs):>12}")
    jogadas = [l["jogadas"] for l in linhas]
    print(f"  jogadas dos agentes por partida (sem contar a abertura): média {statistics.mean(jogadas):.1f}, mín {min(jogadas)}, máx {max(jogadas)}")


if __name__ == "__main__":
    aberturas = gerar_aberturas(N_ABERTURAS, PLIES_ABERTURA, SEMENTE)
    print(f"{len(aberturas)} aberturas distintas de {PLIES_ABERTURA} jogadas (semente {SEMENTE})")

    confrontos = [
        ("AB d=6 vs aleatório", lambda: criar_agente_alfabeta(6), lambda: criar_agente_aleatorio(SEMENTE)),
        ("AB d=6 vs AB d=3",    lambda: criar_agente_alfabeta(6), lambda: criar_agente_alfabeta(3)),
        ("AB d=3 vs aleatório", lambda: criar_agente_alfabeta(3), lambda: criar_agente_aleatorio(SEMENTE)),
    ]
    todas = []
    for nome, fp, fa in confrontos:
        linhas = confronto(nome, fp, fa, aberturas)
        resumo(nome, linhas)
        todas += linhas

    with open("resultados.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=todas[0].keys())
        w.writeheader()
        w.writerows(todas)
    print("\nResultados por partida salvos em resultados.csv")

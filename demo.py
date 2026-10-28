#AB d=6 como X contra AB d=3 como O
import random
from jogo import Jogo
from busca import criar_agente_alfabeta

random.seed(42)
x, o = criar_agente_alfabeta(6), criar_agente_alfabeta(3)
agentes = {1: x, 2: o}
nome = {1: "X (d=6)", 2: "O (d=3)"}
total = {1: 0, 2: 0}

j = Jogo()
for _ in range(4):
    j.jogar(random.choice(j.acoes()))
print("Abertura sorteada:\n" + str(j))

while not j.terminal():
    c, n = agentes[j.vez](j)
    total[j.vez] += n
    print(f"\n{nome[j.vez]} joga na coluna {c} | nós nesta jogada: {n:,} | total do jogador: {total[j.vez]:,}")
    j.jogar(c)
    print(j)

print("\nFim:", {0: "empate", 1: "X venceu", 2: "O venceu"}[j.vencedor])
print(f"Nós totais -> X (d=6): {total[1]:,} | O (d=3): {total[2]:,}")

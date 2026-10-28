# Peças: 0 = vazio, 1 = X (MAX), 2 = O (MIN)
class Jogo:
    def __init__(self, linhas=6, colunas=7, k=4):
        self.L = linhas
        self.C = colunas
        self.K = k
        self.tab = [0] * (linhas * colunas)   # posição = linha * C + coluna, linha 0 é a de baixo
        self.altura = [0] * colunas           # peças em cada coluna
        self.vez = 1
        self.n_jogadas = 0
        self.vencedor = 0
        # colunas do centro primeiro: 3, 2, 4, 1, 5, 0, 6
        self.ordem = sorted(range(colunas), key=lambda c: (abs(c - (colunas - 1) / 2), c))
        self.janelas = self._calcular_janelas()

    def _calcular_janelas(self):
        # todas as sequências de K casas, usadas na avaliação
        janelas = []
        for r in range(self.L):
            for c in range(self.C):
                for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                    rf = r + (self.K - 1) * dr
                    cf = c + (self.K - 1) * dc
                    if 0 <= rf < self.L and 0 <= cf < self.C:
                        janelas.append([(r + i * dr) * self.C + (c + i * dc) for i in range(self.K)])
        return janelas

    def acoes(self):
        return [c for c in self.ordem if self.altura[c] < self.L]

    def jogar(self, c):
        r = self.altura[c]
        self.tab[r * self.C + c] = self.vez
        self.altura[c] += 1
        self.n_jogadas += 1
        if self._ganhou(r, c, self.vez):
            self.vencedor = self.vez
        self.vez = 3 - self.vez

    def desfazer(self, c):
        self.altura[c] -= 1
        self.tab[self.altura[c] * self.C + c] = 0
        self.n_jogadas -= 1
        self.vez = 3 - self.vez
        self.vencedor = 0

    def terminal(self):
        return self.vencedor != 0 or self.n_jogadas == self.L * self.C

    def utilidade(self):
        # +1 se X vence, -1 se O vence, 0 se empata
        return {0: 0, 1: 1, 2: -1}[self.vencedor]

    def _ganhou(self, r, c, j):
        # só olha em volta da última peça jogada
        for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
            n = 1
            for sinal in (1, -1):
                rr = r + sinal * dr
                cc = c + sinal * dc
                while 0 <= rr < self.L and 0 <= cc < self.C and self.tab[rr * self.C + cc] == j:
                    n += 1
                    rr += sinal * dr
                    cc += sinal * dc
            if n >= self.K:
                return True
        return False

    def __str__(self):
        simb = {0: ".", 1: "X", 2: "O"}
        linhas = []
        for r in range(self.L - 1, -1, -1):
            linhas.append(" ".join(simb[self.tab[r * self.C + c]] for c in range(self.C)))
        return "\n".join(linhas) + "\n" + " ".join(str(c) for c in range(self.C))
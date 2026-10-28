"""Ligue 4 (Connect Four). Estado, AÇÕES, RESULTADO, TESTE-TERMINAL e UTILIDADE.

Parametrizado (linhas, colunas, k) para podermos testar em tabuleiros pequenos.
Padrão do trabalho: 6 linhas x 7 colunas, k = 4.

Peças: 0 = vazio, 1 = X (MAX), 2 = O (MIN).
Por eficiência, o estado é alterado "no lugar": jogar(c) aplica o RESULTADO
e desfazer(c) volta ao estado anterior (a busca usa os dois).
"""


class Jogo:
    def __init__(self, linhas=6, colunas=7, k=4):
        self.L, self.C, self.K = linhas, colunas, k
        self.tab = [0] * (linhas * colunas)   # índice = linha * C + coluna (linha 0 = embaixo)
        self.altura = [0] * colunas           # quantas peças há em cada coluna
        self.vez = 1                          # de quem é a vez (faz parte do estado)
        self.n_jogadas = 0
        self.vencedor = 0                     # 0 = ninguém (ainda)
        # ordem das colunas: centro primeiro (3, 2, 4, 1, 5, 0, 6 no 6x7)
        self.ordem = sorted(range(colunas), key=lambda c: (abs(c - (colunas - 1) / 2), c))
        self.janelas = self._calcular_janelas()

    def _calcular_janelas(self):
        """Todas as sequências de k casas (usadas na função de avaliação)."""
        janelas = []
        for r in range(self.L):
            for c in range(self.C):
                for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                    rf, cf = r + (self.K - 1) * dr, c + (self.K - 1) * dc
                    if 0 <= rf < self.L and 0 <= cf < self.C:
                        janelas.append([(r + i * dr) * self.C + (c + i * dc) for i in range(self.K)])
        return janelas

    # ---------- componentes da formalização ----------
    def acoes(self):
        """AÇÕES(s): colunas não cheias, com o centro primeiro."""
        return [c for c in self.ordem if self.altura[c] < self.L]

    def jogar(self, c):
        """RESULTADO(s, c): põe a peça da vez na coluna c e passa a vez."""
        r = self.altura[c]
        self.tab[r * self.C + c] = self.vez
        self.altura[c] += 1
        self.n_jogadas += 1
        if self._ganhou(r, c, self.vez):
            self.vencedor = self.vez
        self.vez = 3 - self.vez

    def desfazer(self, c):
        """Desfaz a última jogada feita na coluna c."""
        self.altura[c] -= 1
        self.tab[self.altura[c] * self.C + c] = 0
        self.n_jogadas -= 1
        self.vez = 3 - self.vez
        self.vencedor = 0

    def terminal(self):
        """TESTE-TERMINAL(s): alguém venceu ou o tabuleiro encheu."""
        return self.vencedor != 0 or self.n_jogadas == self.L * self.C

    def utilidade(self):
        """UTILIDADE(s, MAX): +1 se X vence, -1 se O vence, 0 se empate."""
        return {0: 0, 1: 1, 2: -1}[self.vencedor]

    # ---------- auxiliares ----------
    def _ganhou(self, r, c, j):
        """A peça que acabou de cair em (r, c) formou k em linha?"""
        for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
            n = 1
            for sinal in (1, -1):
                rr, cc = r + sinal * dr, c + sinal * dc
                while 0 <= rr < self.L and 0 <= cc < self.C and self.tab[rr * self.C + cc] == j:
                    n += 1
                    rr, cc = rr + sinal * dr, cc + sinal * dc
            if n >= self.K:
                return True
        return False

    def __str__(self):
        simb = {0: ".", 1: "X", 2: "O"}
        linhas = [" ".join(simb[self.tab[r * self.C + c]] for c in range(self.C))
                  for r in range(self.L - 1, -1, -1)]
        return "\n".join(linhas) + "\n" + " ".join(str(c) for c in range(self.C))

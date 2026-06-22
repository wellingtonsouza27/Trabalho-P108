import math


class PriorityQueue:

    def __init__(
        self,
        lambdas: list[float],
        mu: float,
        s: int,
        preemptive: bool
    ):

        if mu <= 0:
            raise ValueError("μ deve ser maior que zero")

        if s < 1:
            raise ValueError("s deve ser >= 1")

        if len(lambdas) == 0:
            raise ValueError("Informe ao menos uma classe")

        if any(l < 0 for l in lambdas):
            raise ValueError("Todas as taxas λ devem ser >= 0")

        self.lambdas = lambdas
        self.mu = mu
        self.s = s
        self.preemptive = preemptive

        self.lambda_total = sum(lambdas)

        rho = self.lambda_total / (s * mu)

        if rho >= 1:
            raise ValueError(
                f"Sistema instável (ρ = {rho:.4f} >= 1)"
            )

    @property
    def rho_total(self):
        return self.lambda_total / (self.s * self.mu)

    @property
    def r(self):
        return self.lambda_total / self.mu

    def _sigma(self, k: int):

        if k <= 0:
            return 0.0

        return sum(self.lambdas[:k]) / (self.s * self.mu)

    # ==================================================
    # M/M/s clássico (Erlang C)
    # ==================================================

    def _mms_W(self, lam):

        s = self.s
        mu = self.mu

        rho = lam / (s * mu)

        if rho >= 1:
            raise ValueError("Sistema instável")

        a = lam / mu

        soma = sum(
            (a ** n) / math.factorial(n)
            for n in range(s)
        )

        termo_final = (
            (a ** s)
            / math.factorial(s)
            * (1 / (1 - rho))
        )

        P0 = 1 / (soma + termo_final)

        Lq = (
            P0
            * (a ** s)
            * rho
            /
            (
                math.factorial(s)
                * ((1 - rho) ** 2)
            )
        )

        Wq = Lq / lam if lam > 0 else 0

        W = Wq + (1 / mu)

        return W

    # ==================================================
    # Sem interrupção
    # ==================================================

    def _base_term(self):

        s = self.s
        mu = self.mu
        lam = self.lambda_total
        r = self.r

        soma = sum(
            (r ** j) / math.factorial(j)
            for j in range(s)
        )

        return (
            (
                math.factorial(s)
                * (s * mu - lam)
                / (r ** s)
            )
            * soma
            + (s * mu)
        )

    def _W_non_preemptive(self, k: int):

        sigma_k_minus_1 = self._sigma(k - 1)
        sigma_k = self._sigma(k)

        base = self._base_term()

        denom = (
            base
            * (1 - sigma_k_minus_1)
            * (1 - sigma_k)
        )

        if denom <= 0:
            raise ValueError(
                f"Denominador inválido para classe {k}"
            )

        return (1 / denom) + (1 / self.mu)

    # ==================================================
    # Com interrupção S = 1
    # ==================================================

    def _W_preemptive_s1(self, k: int):

        sigma_k_minus_1 = self._sigma(k - 1)
        sigma_k = self._sigma(k)

        denom = (
            (1 - sigma_k_minus_1)
            * (1 - sigma_k)
        )

        if denom <= 0:
            raise ValueError(
                f"Denominador inválido para classe {k}"
            )

        return (1 / self.mu) / denom

    # ==================================================
    # Com interrupção S > 1
    # Método utilizado nos slides
    # ==================================================

    def _W_preemptive_multi_server(self):

        Ws = []

        for k in range(len(self.lambdas)):

            lambda_acumulado = sum(
                self.lambdas[:k + 1]
            )

            W_bar = self._mms_W(
                lambda_acumulado
            )

            if k == 0:

                Ws.append(W_bar)

            else:

                soma = 0

                for i in range(k):

                    soma += (
                        self.lambdas[i]
                        * Ws[i]
                    )

                Wk = (
                    lambda_acumulado * W_bar
                    - soma
                ) / self.lambdas[k]

                Ws.append(Wk)

        return Ws

    # ==================================================
    # Resultados
    # ==================================================

    def results(self):

        resultados = []

        # ----------------------------------------------
        # COM INTERRUPÇÃO E S > 1
        # ----------------------------------------------

        if self.preemptive and self.s > 1:

            Ws = self._W_preemptive_multi_server()

            for k, lam_k in enumerate(
                self.lambdas,
                start=1
            ):

                W = Ws[k - 1]

                Wq = W - (1 / self.mu)

                lambda_acumulado = sum(
                    self.lambdas[:k]
                )

                L = lambda_acumulado * W

                Lq = (
                    L
                    - (lambda_acumulado / self.mu)
                )

                resultados.append({
                    "classe": k,
                    "lambda": lam_k,
                    "W": W,
                    "Wq": Wq,
                    "L": L,
                    "Lq": Lq
                })

            return resultados

        # ----------------------------------------------
        # S = 1 ou SEM INTERRUPÇÃO
        # ----------------------------------------------

        for k, lam_k in enumerate(
            self.lambdas,
            start=1
        ):

            if self.preemptive:

                W = self._W_preemptive_s1(k)

            else:

                W = self._W_non_preemptive(k)

            Wq = W - (1 / self.mu)

            if self.preemptive:

                lambda_acumulado = sum(
                    self.lambdas[:k]
                )

                L = lambda_acumulado * W

                Lq = (
                    L
                    - (lambda_acumulado / self.mu)
                )

            else:

                L = lam_k * W

                Lq = (
                    L
                    - (lam_k / self.mu)
                )

            resultados.append({
                "classe": k,
                "lambda": lam_k,
                "W": W,
                "Wq": Wq,
                "L": L,
                "Lq": Lq
            })

        return resultados
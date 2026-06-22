import math


class PriorityQueue:

    def __init__(self, lambdas: list[float], mu: float, s: int, preemptive: bool):

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

    def _W_k(self, k: int):

        sigma_k_minus_1 = self._sigma(k - 1)
        sigma_k = self._sigma(k)

        if self.preemptive:

            denom = (
                (1 - sigma_k_minus_1)
                * (1 - sigma_k)
            )

            if denom <= 0:
                raise ValueError(
                    f"Denominador inválido para classe {k}"
                )

            return (1 / self.mu) / denom

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

    def results(self):

        resultados = []

        for k, lam_k in enumerate(
            self.lambdas,
            start=1
        ):

            W = self._W_k(k)

            Wq = W - (1 / self.mu)

            # Slides:
            # L = λW
            # Lq = L - λ/μ

            L = lam_k * W

            Lq = L - (lam_k / self.mu)

            resultados.append({
                "classe": k,
                "lambda": lam_k,
                "W": W,
                "Wq": Wq,
                "L": L,
                "Lq": Lq
            })

        return resultados
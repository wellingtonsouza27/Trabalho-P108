import math


class MMS:

    def __init__(self, lambda_, mi, s):
        if lambda_ <= 0:
            raise ValueError("λ deve ser maior que zero")

        if mi <= 0:
            raise ValueError("μ deve ser maior que zero")

        if s < 2:
            raise ValueError("s deve ser >= 2")

        self._lambda_ = lambda_
        self._mi = mi
        self._s = int(s)

        if self.rho >= 1:
            raise ValueError("Sistema instável (ρ >= 1)")

    @property
    def rho(self):
        return self._lambda_ / (self._s * self._mi)

    @property
    def a(self):
        return self._lambda_ / self._mi

    @property
    def p0(self):
        soma = 0

        for n in range(self._s):
            soma += (self.a ** n) / math.factorial(n)

        termo_final = ((self.a ** self._s) / math.factorial(self._s)) * (
            1 / (1 - self.rho)
        )

        return 1 / (soma + termo_final)

    def prob_n(self, n):
        if n < 0:
            raise ValueError("n deve ser >= 0")

        if n <= self._s:
            return ((self.a ** n) / math.factorial(n)) * self.p0
        else:
            return ((self.a ** n) / (
                math.factorial(self._s) * (self._s ** (n - self._s))
            )) * self.p0

    def avg_clients_queue(self):
        return (
            self.p0
            * (self.a ** self._s)
            * self.rho
            / (math.factorial(self._s) * ((1 - self.rho) ** 2))
        )

    def avg_time_queue(self):
        return self.avg_clients_queue() / self._lambda_

    def avg_clients_system(self):
        return self.avg_clients_queue() + self.a

    def avg_time_system(self):
        return self.avg_time_queue() + (1 / self._mi)

    def prob_wait_queue_zero(self):
        soma = 0
        for n in range(self._s):
            soma += self.prob_n(n)
        return soma

    def prob_wait_queue_greater_than(self, t):
        if t < 0:
            raise ValueError("t deve ser >= 0")

        return (
            (1 - self.prob_wait_queue_zero())
            * math.exp(-self._s * self._mi * (1 - self.rho) * t)
        )

    def prob_wait_system_greater_than(self, t):
        if t < 0:
            raise ValueError("t deve ser >= 0")

        return math.exp(-self._mi * t)

    def summary(self):
        print("=== RESUMO - Fila M/M/s ===")
        print(f"λ = {self._lambda_:.4f}")
        print(f"μ = {self._mi:.4f}")
        print(f"s = {self._s}")
        print(f"ρ = {self.rho:.4f}")
        print(f"P0 = {self.p0:.4f}")
        print(f"Lq = {self.avg_clients_queue():.4f}")
        print(f"Wq = {self.avg_time_queue():.4f}")
        print(f"L = {self.avg_clients_system():.4f}")
        print(f"W = {self.avg_time_system():.4f}")
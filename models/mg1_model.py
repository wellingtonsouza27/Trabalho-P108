class MG1:

    def __init__(self, lambda_, mi):

        if mi <= 0:
            raise ValueError("μ deve ser maior que zero")

        rho = lambda_ / mi

        if rho >= 1:
            raise ValueError("Sistema instável (ρ >= 1)")

        self.lambda_ = lambda_
        self.mi = mi

    @property
    def rho(self):
        return self.lambda_ / self.mi

    @property
    def p0(self):
        return 1 - self.rho

    @property
    def sigma2(self):
        return (1 / self.mi) ** 2

    def avg_clients_queue(self):
        return (
            (self.lambda_ ** 2) * self.sigma2 +
            self.rho ** 2
        ) / (2 * (1 - self.rho))

    def avg_time_queue(self):
        return self.avg_clients_queue() / self.lambda_

    def avg_clients_system(self):
        return self.avg_clients_queue() + self.rho

    def avg_time_system(self):
        return self.avg_time_queue() + (1 / self.mi)
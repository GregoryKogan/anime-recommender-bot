import random


class Formula(object):
    def __init__(self, factors_amount=1, start_factors=None):
        if not start_factors:
            self.factors = [(random.random() * 2 - 1) for _ in range(factors_amount)]
        else:
            self.factors = start_factors

    def get_output(self, args):
        if len(args) != len(self.factors):
            print('Unequal number of factors and arguments!')
            return None
        result = 0
        for i in range(len(args)):
            result += args[i] * self.factors[i]
        return result

    @staticmethod
    def mutate(origin, mutation_rate):
        result = Formula(start_factors=origin.factors.copy())
        for i in range(len(result.factors)):
            mutation = (random.random() * 2 - 1) * mutation_rate
            result.factors[i] += mutation
        return result


class Guesser(object):
    def __init__(self, args, target, precision=0.01, mutation_rate=0.01, population_size=1000):
        self.arguments = args
        self.target = target
        self.precision = precision
        self.mutation_rate = mutation_rate
        self.population_size = population_size
        
        self.formulas = [Formula(factors_amount=len(args)) for _ in range(population_size)]

    def test_formulas(self):
        result = []
        for formula in self.formulas:
            output = formula.get_output(self.arguments)
            error = abs(self.target - output)
            record = {
                'formula': formula,
                'error': error
            }
            result.append(record)
        result.sort(key=lambda i: i['error'])
        return result

    def train(self):
        current_gen = self.test_formulas()
        next_gen = []
        for i in range(self.population_size // 2):
            next_gen.append(current_gen[i]['formula'])

        for i in range(self.population_size // 2):
            origin = current_gen[i]['formula']
            child = Formula.mutate(origin, self.mutation_rate)
            next_gen.append(child)

        self.formulas = next_gen.copy()


if __name__ == '__main__':
    precision = 0.001
    g = Guesser([420, 69, 1337], 69, mutation_rate=0.001, population_size=2)
    best = g.test_formulas()[0]
    print(best['formula'].factors)
    print(best['error'])
    while best['error'] > precision:
        g.train()
        best = g.test_formulas()[0]
        print(f'Error: {best["error"]}')
    best = g.test_formulas()[0]
    print(best['formula'].factors)
    print(best['error'])

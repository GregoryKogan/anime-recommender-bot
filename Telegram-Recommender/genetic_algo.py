import random


class Formula(object):
    def __init__(self, factors_amount=1, start_factors=None):
        self.factors = start_factors or [
            ((random.random() * 2) - 1) for _ in range(factors_amount)
        ]

    def get_output(self, args):
        if len(args) != len(self.factors):
            print('Unequal number of factors and arguments!')
            return None
        return sum(args[i] * self.factors[i] for i in range(len(args)))

    @staticmethod
    def mutate(origin, mutation_rate):
        result = Formula(start_factors=origin.factors.copy())
        for i in range(len(result.factors)):
            mutation = (random.random() * 2 - 1) * mutation_rate
            result.factors[i] += mutation
        return result


class Guesser(object):
    def __init__(self, factors_amount, mutation_rate=0.01, population_size=1000):
        self.factors_amount = factors_amount
        self.mutation_rate = mutation_rate
        self.population_size = population_size
        self.precision = 1e9

        self.formulas = [Formula(factors_amount=factors_amount) for _ in range(population_size)]

    def test_formulas(self, training_data):
        result = [{}] * len(self.formulas)
        for data_sample in training_data:
            for formula_num, formula in enumerate(self.formulas):
                output = formula.get_output(data_sample['Input'])
                error = abs(data_sample['Target'] - output)
                if len(result[formula_num]) == 0:
                    result[formula_num] = {
                        'formula': formula,
                        'error': 0
                    }
                result[formula_num]['error'] += error
        result.sort(key=lambda i: i['error'])
        self.precision = result[0]['error'] / len(training_data)
        return result

    def train(self, training_data):
        current_gen = self.test_formulas(training_data)
        next_gen = [
            current_gen[survived_ind]['formula']
            for survived_ind in range(self.population_size // 2)
        ]

        for new_born_ind in range(self.population_size // 2):
            origin = current_gen[new_born_ind]['formula']
            child = Formula.mutate(origin, self.mutation_rate)
            next_gen.append(child)

        self.formulas = next_gen.copy()


if __name__ == '__main__':
    training_data = [
        {
            'Input': [123, 553, 678],
            'Target': 79
        },
        {
            'Input': [479, 296, 46],
            'Target': 89
        },
        {
            'Input': [123, 984, 190],
            'Target': 78
        }
    ]

    g = Guesser(3, mutation_rate=0.01, population_size=1000)
    while g.precision > 1:
        g.train(training_data)
        best = g.test_formulas(training_data)[0]
        print(g.precision)
        print(best['formula'].factors)

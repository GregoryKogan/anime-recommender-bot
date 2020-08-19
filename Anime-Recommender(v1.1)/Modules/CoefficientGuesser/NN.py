class Matrix:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns

        self.values = [[0 for _ in range(self.columns)] for _ in range(self.rows)]

    def print(self):
        print('=' * (5 * self.columns + 1))
        for row in self.values:
            line = '|'
            for cell in row:
                if cell < 0:
                    cell_text = str(round(cell, 1)) + '|'
                else:
                    cell_text = str(round(cell, 2)) + '|'
                    if len(cell_text) == 4:
                        cell_text = str(round(cell, 2)) + ' |'
                line += cell_text
            print(line)
        print('=' * (5 * self.columns + 1))
        print('')

    @staticmethod
    def multiply(m1, m2):
        if m1.columns != m2.rows:
            return None
        result = Matrix(m1.rows, m2.columns)
        for i in range(result.rows):
            for j in range(result.columns):
                cell = 0
                for k in range(m1.columns):
                    cell += m1.values[i][k] * m2.values[k][j]
                result.values[i][j] = cell
        return result

    def multiply_this(self, n):
        if type(n) is Matrix:
            for i in range(self.rows):
                for j in range(self.columns):
                    self.values[i][j] *= n.values[i][j]
        else:
            for i in range(self.rows):
                for j in range(self.columns):
                    self.values[i][j] *= n

    def fill_random(self):
        import random
        for i in range(self.rows):
            for j in range(self.columns):
                self.values[i][j] = random.random() * 2 - 1

    def self_copy(self):
        return self.values.copy()

    @staticmethod
    def transpose(m):
        result = Matrix(m.columns, m.rows)
        for i in range(m.rows):
            for j in range(m.columns):
                result.values[j][i] = m.values[i][j]
        return result

    def add(self, n):
        if type(n) is Matrix:
            for i in range(self.rows):
                for j in range(self.columns):
                    self.values[i][j] += n.values[i][j]
        else:
            for i in range(self.rows):
                for j in range(self.columns):
                    self.values[i][j] += n

    @staticmethod
    def subtract(m1, m2):
        result = Matrix(m1.rows, m1.columns)
        for i in range(result.rows):
            for j in range(result.columns):
                result.values[i][j] = m1.values[i][j] - m2.values[i][j]
        return result

    @staticmethod
    def apply_function(m, func):
        result = Matrix(m.rows, m.columns)
        for i in range(m.rows):
            for j in range(m.columns):
                value = m.values[i][j]
                result.values[i][j] = func(value)
        return result

    @staticmethod
    def make_array(input_matrix):
        result = []
        for i in range(input_matrix.rows):
            for j in range(input_matrix.columns):
                result.append(input_matrix.values[i][j])
        return result

    @staticmethod
    def make_matrix(input_array):
        result = Matrix(len(input_array), 1)
        for i in range(len(input_array)):
            result.values[i][0] = input_array[i]
        return result


def sigmoid(x):
    import math
    return 1 / (1 + math.exp(-x))


def sigmoid_derivative(s):
    return s * (1 - s)


class Specification:
    def __init__(self):
        self.input_num = 1
        self.output_num = 1
        self.hidden_layers_num = 1
        self.hidden_num = [1]
        self.learning_rate = 0.01

    def set_options(self, input_num, output_num, hidden_layers_num, hidden_num, learning_rate):
        self.input_num = input_num
        self.output_num = output_num
        self.hidden_layers_num = hidden_layers_num
        self.hidden_num = hidden_num
        self.learning_rate = learning_rate


class NeuralNetwork:
    def __init__(self):
        self.num_of_input_neurons = None
        self.num_of_output_neurons = None
        self.num_of_hidden_layers = None
        self.num_of_hidden_neurons_per_layer = None
        self.weights = []
        self.biases = []
        self.learning_rate = None

    def set_specs(self, specs):
        self.num_of_input_neurons = specs.input_num
        self.num_of_output_neurons = specs.output_num
        self.num_of_hidden_layers = specs.hidden_layers_num
        self.num_of_hidden_neurons_per_layer = specs.hidden_num
        self.learning_rate = specs.learning_rate

        self.weights = []
        for i in range(self.num_of_hidden_layers + 1):
            if i == 0:
                weights_i = Matrix(self.num_of_hidden_neurons_per_layer[0], self.num_of_input_neurons)
            elif i == self.num_of_hidden_layers:
                weights_i = Matrix(self.num_of_output_neurons,
                                   self.num_of_hidden_neurons_per_layer[self.num_of_hidden_layers - 1])
            else:
                weights_i = Matrix(self.num_of_hidden_neurons_per_layer[i], self.num_of_hidden_neurons_per_layer[i - 1])
            weights_i.fill_random()
            self.weights.append(weights_i)

        self.biases = []
        for i in range(self.num_of_hidden_layers):
            bias_i = Matrix(self.num_of_hidden_neurons_per_layer[i], 1)
            bias_i.fill_random()
            self.biases.append(bias_i)
        bias_o = Matrix(self.num_of_output_neurons, 1)
        bias_o.fill_random()
        self.biases.append(bias_o)

    def predict(self, input_array):
        input_matrix = Matrix.make_matrix(input_array)

        first_hidden = Matrix.multiply(self.weights[0], input_matrix)
        first_hidden.add(self.biases[0])
        first_hidden = Matrix.apply_function(first_hidden, sigmoid)

        previous_result = first_hidden

        for i in range(1, self.num_of_hidden_layers):
            hidden_i = Matrix.multiply(self.weights[i], previous_result)
            hidden_i.add(self.biases[i])
            hidden_i = Matrix.apply_function(hidden_i, sigmoid)
            previous_result = hidden_i

        output = Matrix.multiply(self.weights[self.num_of_hidden_layers], previous_result)
        output.add(self.biases[self.num_of_hidden_layers])
        output = Matrix.apply_function(output, sigmoid)

        return Matrix.make_array(output)

    def train(self, input_array, answer):
        layers_results = []
        input_matrix = Matrix.make_matrix(input_array)

        first_hidden = Matrix.multiply(self.weights[0], input_matrix)
        first_hidden.add(self.biases[0])
        first_hidden = Matrix.apply_function(first_hidden, sigmoid)

        previous_result = first_hidden
        layers_results.append(first_hidden)

        for i in range(1, self.num_of_hidden_layers):
            hidden_i = Matrix.multiply(self.weights[i], previous_result)
            hidden_i.add(self.biases[i])
            hidden_i = Matrix.apply_function(hidden_i, sigmoid)
            previous_result = hidden_i
            layers_results.append(hidden_i)

        output = Matrix.multiply(self.weights[self.num_of_hidden_layers], previous_result)
        output.add(self.biases[self.num_of_hidden_layers])
        output = Matrix.apply_function(output, sigmoid)
        layers_results.append(output)

        target = Matrix.make_matrix(answer)
        output_error = Matrix.subtract(target, output)
        next_error = output_error
        gradient = Matrix.apply_function(output, sigmoid_derivative)
        gradient.multiply_this(output_error)
        gradient.multiply_this(self.learning_rate)
        transposed_last_hidden = Matrix.transpose(previous_result)
        weight_delta_ho = Matrix.multiply(gradient, transposed_last_hidden)
        self.weights[self.num_of_hidden_layers].add(weight_delta_ho)
        self.biases[self.num_of_hidden_layers].add(gradient)

        for i in range(self.num_of_hidden_layers - 1, -1, -1):
            next_weights_transposed = Matrix.transpose(self.weights[i + 1])
            hidden_error_i = Matrix.multiply(next_weights_transposed, next_error)
            next_error = hidden_error_i
            hidden_gradient_i = Matrix.apply_function(layers_results[i], sigmoid_derivative)
            hidden_gradient_i.multiply_this(hidden_error_i)
            hidden_gradient_i.multiply_this(self.learning_rate)
            if i > 0:
                transposed_previous = Matrix.transpose(layers_results[i - 1])
            else:
                transposed_previous = Matrix.transpose(input_matrix)
            weight_delta_i = Matrix.multiply(hidden_gradient_i, transposed_previous)
            self.weights[i].add(weight_delta_i)
            self.biases[i].add(hidden_gradient_i)


if __name__ == '__main__':
    training_data = [
        {
            'Inputs': [0, 1],
            'Targets': [1]
        },
        {
            'Inputs': [1, 0],
            'Targets': [1]
        },
        {
            'Inputs': [0, 0],
            'Targets': [0]
        },
        {
            'Inputs': [1, 1],
            'Targets': [0]
        },
    ]

    learning_rate = float(input('Learning rate: '))
    accuracy = float(input('Accuracy: '))

    nn_specs = Specification()
    nn_specs.set_options(2, 1, 2, [5, 4], learning_rate)
    brain = NeuralNetwork()
    brain.set_specs(nn_specs)

    average_error = 1e9
    last_10_results = []
    import random

    import time

    begin = time.process_time()
    epochs = 1
    while average_error > accuracy:
        if epochs % 1000 == 0:
            print(f'{epochs} epochs, average error: {average_error}')
        data = random.choice(training_data)
        prediction = brain.predict(data['Inputs'])[0]
        last_10_results.append(abs(prediction - data['Targets'][0]))
        if len(last_10_results) > 10:
            last_10_results = last_10_results[1:]
        sum_of_errors = 0
        for error in last_10_results:
            sum_of_errors += error
        average_error = sum_of_errors / len(last_10_results)
        brain.train(data['Inputs'], data['Targets'])
        epochs += 1
    end = time.process_time()

    print('=======')
    print(round(brain.predict([1, 0])[0], 5))
    print(round(brain.predict([0, 1])[0], 5))
    print(round(brain.predict([1, 1])[0], 5))
    print(round(brain.predict([0, 0])[0], 5))
    print('=======')
    print(f'Finished in {end - begin}(s)')

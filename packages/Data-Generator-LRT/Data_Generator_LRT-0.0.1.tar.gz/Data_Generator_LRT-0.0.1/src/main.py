#this code sets up a restricted data set generator for use in a project focused on machine learning methods centered
#centered around linear regression.

import numpy as np

class data_set_generator:
    x_1 = np.random.randint(low=1, high=20, size=100)
    x_2 = np.random.randint(low=1, high=20, size=100)
    x_3 = np.random.randint(low=1, high=20, size=100)

    def __init__(self):
        self.intercept = np.random.randint(low=1, high=20, size=1)
        self.X_0 = np.column_stack([x_1, x_2, x_3])

    def calculate_y(self, weight_1, weight_2, weight_3):
        linear_y = [weight_1 * x for x in x_1]
        linear_y_2 = [linear_y[i] + weight_2 * x_2[i] for i in range(0, len(x_2))]
        linear_y_3 = [linear_y_2[i] - weight_3 * x_3[i] for i in range(0, len(x_3))]
        self.linear_y = np.array(linear_y_3) + self.intercept
        noise = noise = np.random.normal(10, 3, 100)
        self.linear_y_noise = [linear_y_3[i] + noise[i] for i in range(0, len(noise))]

    def for_josh():
        print('Fuck You')

data = data_set_generator

print(data)
import numpy as np

class NeuralNetwork:
    def __init__(self, input_dim, hidden_dim, output_dim):
        self.weights1 = np.random.randn(input_dim, hidden_dim) * 0.01
        self.bias1 = np.zeros((1, hidden_dim))
        self.weights2 = np.random.randn(hidden_dim, output_dim) * 0.01
        self.bias2 = np.zeros((1, output_dim))

    def forward(self, x):
        self.z1 = np.dot(x, self.weights1) + self.bias1
        self.a1 = np.tanh(self.z1)
        self.z2 = np.dot(self.a1, self.weights2) + self.bias2
        return self.z2

    def backward(self, x, grad_output, learning_rate):
        grad_z2 = grad_output
        grad_weights2 = np.dot(self.a1.T, grad_z2)
        grad_bias2 = np.sum(grad_z2, axis=0, keepdims=True)
        
        grad_a1 = np.dot(grad_z2, self.weights2.T)
        grad_z1 = grad_a1 * (1 - np.tanh(self.z1)**2)
        grad_weights1 = np.dot(x.T, grad_z1)
        grad_bias1 = np.sum(grad_z1, axis=0, keepdims=True)
        
        self.weights1 -= learning_rate * grad_weights1
        self.bias1 -= learning_rate * grad_bias1
        self.weights2 -= learning_rate * grad_weights2
        self.bias2 -= learning_rate * grad_bias2

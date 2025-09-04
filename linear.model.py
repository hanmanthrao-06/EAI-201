import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

X = np.linspace(-10, 10, 100)
Y = 2 * X + 3 + np.random.randn(*X.shape) * 2  

model = tf.keras.Sequential([
    tf.keras.Input(shape=(1,)),
    tf.keras.layers.Dense(1)  
])

model.compile(optimizer='sgd', loss='mean_squared_error')

model.fit(X, Y, epochs=200, verbose=0)

Y_pred = model.predict(X)

weights, bias = model.layers[0].get_weights()
print(f"Learned slope (m): {weights[0][0]:.2f}")
print(f"Learned intercept (c): {bias[0]:.2f}")

plt.scatter(X, Y, label="Original Data")
plt.plot(X, Y_pred, color="red", label="Fitted Line")
plt.legend()
plt.show()

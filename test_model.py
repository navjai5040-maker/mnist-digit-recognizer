import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model('mnist_model.keras')

sample = np.zeros((1, 28, 28), dtype=np.float32)

prediction = model.predict(sample, verbose=0)

print("Model loaded!")
print("Prediction:", prediction.argmax(axis=1)[0])
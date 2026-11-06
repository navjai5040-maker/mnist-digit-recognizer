# MNIST Handwritten Digit Recognizer

A handwritten digit recognition web application built using Python, TensorFlow, Keras, Flask, HTML, CSS and JavaScript.

## Features
- Interactive drawing canvas
- Handwritten digit recognition (0–9)
- Image preprocessing using Pillow and NumPy
- Centre-of-mass alignment
- Real-time prediction through a Flask API

## Model Architecture
- Flatten layer
- Dense layer with 128 neurons and ReLU activation
- Dense output layer with 10 neurons and Softmax activation

## Model Performance
- MNIST test accuracy: 97.83%

## Tech Stack
- Python 3.13
- TensorFlow 2.21
- Keras
- Flask
- NumPy
- Pillow
- HTML, CSS and JavaScript

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
python app.py
```

Open `http://127.0.0.1:5000/` in your browser.

## Future Improvements
- Experiment with CNN architectures
- Improve preprocessing
- Explore data augmentation
- Improve generalization to real-world handwriting
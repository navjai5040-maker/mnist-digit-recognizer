
from flask import Flask, render_template, request, jsonify
from tensorflow import keras

from PIL import Image
from io import BytesIO
from pathlib import Path

import numpy as np
import base64
import binascii


# ==========================================
# 1. INITIALIZE FLASK APPLICATION
# ==========================================

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024


# ==========================================
# 2. LOAD TRAINED MODEL
# ==========================================

MODEL_PATH = Path(__file__).resolve().parent / 'mnist_model.keras'

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model file not found: {MODEL_PATH}\n"
        "Place mnist_model.keras in the project root directory."
    )

model = keras.models.load_model(MODEL_PATH)

print("MNIST model loaded successfully!")


# ==========================================
# 3. IMAGE PREPROCESSING
# ==========================================


def preprocess_image(image_data):

    # 1. Decode the Base64 image
    if not image_data.startswith('data:image/png;base64,'):
        raise ValueError("Invalid image format.")

    encoded_data = image_data.split(',', 1)[1]

    image_bytes = base64.b64decode(
        encoded_data,
        validate=True
    )

    # 2. Convert to grayscale
    image = Image.open(BytesIO(image_bytes)).convert('L')

    # 3. Crop the digit
    bbox = image.getbbox()

    if bbox is None:
        raise ValueError("No digit detected. Please draw a digit.")

    image = image.crop(bbox)

    # 4. Resize proportionally to fit 20x20
    image.thumbnail(
        (20, 20),
        Image.Resampling.LANCZOS
    )

    # 5. Place on a 28x28 black canvas
    processed_image = Image.new('L', (28, 28), 0)

    x = (28 - image.width) // 2
    y = (28 - image.height) // 2

    processed_image.paste(image, (x, y))

    # 6. Convert to NumPy array
    image_array = np.array(
        processed_image,
        dtype=np.float32
    )

    # 7. Calculate centre of mass
    total_intensity = np.sum(image_array)

    if total_intensity == 0:
        raise ValueError("No digit detected.")

    y_indices, x_indices = np.indices(image_array.shape)

    center_x = np.sum(x_indices * image_array) / total_intensity
    center_y = np.sum(y_indices * image_array) / total_intensity

    # 8. Calculate required shift
    target_center = 13.5

    shift_x = target_center - center_x
    shift_y = target_center - center_y

    # 9. Shift the image using PIL affine transformation
    processed_image = processed_image.transform(
        (28, 28),
        Image.Transform.AFFINE,
        (1, 0, -shift_x, 0, 1, -shift_y),
        resample=Image.Resampling.BICUBIC
    )

    # 10. Normalize pixel values
    image_array = np.array(
        processed_image,
        dtype=np.float32
    ) / 255.0

    # 11. Add batch dimension
    image_array = image_array.reshape(1, 28, 28)

    return image_array


# ==========================================
# 4. HOME PAGE
# ==========================================

@app.route('/')
def home():
    return render_template('index.html')


# ==========================================
# 5. PREDICTION ENDPOINT
# ==========================================

@app.route('/predict', methods=['POST'])
def predict():

    data = request.get_json(silent=True)

    if not data or 'image' not in data:
        return jsonify({
            'error': 'No image received.'
        }), 400

    try:

        # Preprocess the incoming image
        image_array = preprocess_image(data['image'])

        # Make prediction
        probabilities = model.predict(
            image_array,
            verbose=0
        )

        # Get digit with highest probability
        predicted_digit = int(
            np.argmax(probabilities, axis=1)[0]
        )

        return jsonify({
            'prediction': predicted_digit
        })

    except (ValueError, binascii.Error) as error:

        return jsonify({
            'error': str(error)
        }), 400

    except Exception as error:

        print("Prediction error:", error)

        return jsonify({
            'error': 'Unable to process the prediction.'
        }), 500


# ==========================================
# 6. RUN APPLICATION
# ==========================================

if __name__ == '__main__':
    app.run(debug=True)

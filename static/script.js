
// ==========================================
// 1. GET HTML ELEMENTS
// ==========================================

const canvas = document.getElementById('digitCanvas');
const ctx = canvas.getContext('2d');

const clearBtn = document.getElementById('clearBtn');
const predictBtn = document.getElementById('predictBtn');

const prediction = document.getElementById('prediction');
const status = document.getElementById('status');

let isDrawing = false;
let hasDrawing = false;


// ==========================================
// 2. INITIALIZE CANVAS
// ==========================================

function initializeCanvas() {
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = 'white';
    ctx.lineWidth = 18;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
}

initializeCanvas();


// ==========================================
// 3. GET POINTER POSITION
// ==========================================

function getPosition(event) {
    const rect = canvas.getBoundingClientRect();

    return {
        x: (event.clientX - rect.left) *
           (canvas.width / rect.width),

        y: (event.clientY - rect.top) *
           (canvas.height / rect.height)
    };
}


// ==========================================
// 4. DRAWING FUNCTIONALITY
// ==========================================

canvas.addEventListener('pointerdown', function(event) {

    isDrawing = true;
    hasDrawing = true;

    canvas.setPointerCapture(event.pointerId);

    const pos = getPosition(event);

    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);

    // Draw a small dot even for a single click
    ctx.lineTo(pos.x + 0.1, pos.y + 0.1);
    ctx.stroke();

    prediction.textContent = '?';
    status.textContent = '';
});


canvas.addEventListener('pointermove', function(event) {

    if (!isDrawing) return;

    const pos = getPosition(event);

    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
});


function stopDrawing() {
    isDrawing = false;
}

canvas.addEventListener('pointerup', stopDrawing);
canvas.addEventListener('pointercancel', stopDrawing);


// ==========================================
// 5. CLEAR CANVAS
// ==========================================

clearBtn.addEventListener('click', function() {

    initializeCanvas();

    hasDrawing = false;

    prediction.textContent = '?';
    status.textContent = '';

    predictBtn.disabled = false;
});


// ==========================================
// 6. SEND DRAWING TO FLASK
// ==========================================

predictBtn.addEventListener('click', async function() {

    if (!hasDrawing) {
        status.textContent = 'Please draw a digit first.';
        return;
    }

    predictBtn.disabled = true;

    status.textContent = 'Predicting...';
    prediction.textContent = '?';

    try {

        // Convert canvas into a Base64 PNG image
        const imageData = canvas.toDataURL('image/png');

        // Send image data to Flask
        const response = await fetch('/predict', {

            method: 'POST',

            headers: {
                'Content-Type': 'application/json'
            },

            body: JSON.stringify({
                image: imageData
            })

        });


        // Convert Flask response into JavaScript object
        const result = await response.json();


        // Check whether Flask returned an error
        if (!response.ok) {
            throw new Error(result.error || 'Prediction failed.');
        }


        // Display predicted digit
        prediction.textContent = result.prediction;

        status.textContent = 'Prediction successful!';

    }

    catch (error) {

        console.error('Prediction error:', error);

        prediction.textContent = '?';
        status.textContent = error.message || 'Something went wrong.';

    }

    finally {

        predictBtn.disabled = false;

    }

});

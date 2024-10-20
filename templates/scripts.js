// Get video element and text display
const videoElement = document.getElementById('videoElement');
const recognizedText = document.getElementById('recognizedText');

// Initialize MediaPipe Hands for hand tracking
const hands = new Hands({locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`});
hands.setOptions({
    maxNumHands: 1,
    minDetectionConfidence: 0.7,
    minTrackingConfidence: 0.7
});
hands.onResults(onResults);

// Load TensorFlow.js model (Replace the URL with your actual model URL)
let model;
tf.loadGraphModel('https://your-model-url/model.json').then(loadedModel => {
    model = loadedModel;
    console.log("Model Loaded");
});

// Handle results from MediaPipe Hands
function onResults(results) {
    if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
        const handLandmarks = results.multiHandLandmarks[0];

        // Preprocess landmarks for the TensorFlow model
        const input = preprocessLandmarks(handLandmarks);

        // Perform inference with the model to recognize the gesture
        model.predict(input).then(predictions => {
            const gesture = interpretPrediction(predictions);
            recognizedText.innerText = `Recognized Sign: ${gesture}`;
        });
    }
}

// Preprocess hand landmarks for the TensorFlow model
function preprocessLandmarks(landmarks) {
    const inputArray = landmarks.map(landmark => [landmark.x, landmark.y, landmark.z]);
    return tf.tensor([inputArray.flat()]); // Flatten and return as Tensor
}

// Interpret the model's output and map it to gestures (words)
function interpretPrediction(predictions) {
    const maxIndex = predictions.argMax(-1).dataSync()[0];
    const gestureLabels = ['Hello', 'Thank You', 'Please', 'Yes', 'No']; // Add more gestures here
    return gestureLabels[maxIndex] || 'Unknown';
}

// Start the camera feed
navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
    videoElement.srcObject = stream;
    videoElement.play();

    // Connect the MediaPipe Hands solution to the video stream
    const camera = new Camera(videoElement, {
        onFrame: async () => {
            await hands.send({image: videoElement});
        },
        width: 640,
        height: 480
    });
    camera.start();
});

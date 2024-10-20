function startListening() {
    // Check if the browser supports speech recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.lang = 'en-US'; // You can set the language here
        recognition.interimResults = false; // Return only final results
        recognition.maxAlternatives = 1;

        recognition.onstart = () => {
            console.log("Listening for speech...");
        };

        recognition.onspeechend = () => {
            console.log("Speech ended.");
            recognition.stop();
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            document.getElementById('textInput').value = transcript;
            console.log("Transcript:", transcript);
        };

        recognition.onerror = (event) => {
            console.error("Speech recognition error detected: " + event.error);
        };

        recognition.start(); // Start listening
    } else {
        alert('Speech recognition is not supported in this browser.');
    }
}
// voice-prompts.js

// Function to handle speech synthesis
function speak(text) {
    var msg = new SpeechSynthesisUtterance();
    msg.text = text;
    msg.lang = 'en-US'; // You can change the language if needed
    window.speechSynthesis.speak(msg);
}

// Function to gather all text content from the page
function getAllTextFromPage() {
    return document.body.innerText; // This will capture all the text from the body of the page
}

// Event listener for the Speak button in the navbar
document.addEventListener('DOMContentLoaded', function() {
    var speakButton = document.getElementById('speakButton');
    if (speakButton) {
        speakButton.addEventListener('click', function() {
            var pageText = getAllTextFromPage();
            speak(pageText);
        });
    }
    
    // Additional event listeners for other elements can be added here...
});
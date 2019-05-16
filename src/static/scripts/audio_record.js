const player = document.querySelector('#player');
let clockFunction;
// Function for reading user audio
navigator.mediaDevices.getUserMedia({ audio: true })
.then(stream => {
    mediaRecorder = new MediaRecorder(stream); 
    let audioChunks = []    // Store audio chunks

    // Push audio data to audioChunks array
    mediaRecorder.addEventListener('dataavailable', e => {
        audioChunks.push(e.data);
    }); 
    // Create event listener for when audio recording stops
    mediaRecorder.addEventListener("stop", () => {
        // Create blob from audioChunks
        const audioBlob = new Blob(audioChunks, {type: 'audio/webm;codecs=opus'});
        // Make POST request to server-side script with audio file
        const req = new XMLHttpRequest;
        req.open('POST', '/audio-upload', true);
        // Handle return from server-side script post audio analysis
        req.onload = function() {
            console.log(req.response)
            // Reset audioChunks array for next read
            audioChunks = [];
            // Parse the server response
            song = req.response.substring(0, req.response.search(';'));
            sgramFile = req.response.substring(req.response.search(';') + 1, req.response.length);
            // Set song name in html #song-name element
            songName = document.querySelector('#song-name');
            songName.textContent = song;
            // Select html elements that need to be modified
            const audioContainer = document.querySelector('#audio-container');
            const sgramContainer = document.querySelector('#sgram-container');
            const audioPlayer = document.querySelector('#audio-player');
            const sgramImage = document.querySelector('#sgram-image');
            // Handle displaying/hiding elements based on server response
            if (!req.response.includes('No Match')) {
                audioPlayer.src = '/static/songs/' + encodeURI(song) + '.mp3';
                sgramImage.src = '/static/' + sgramFile;
                audioPlayer.load();
                audioContainer.classList.remove('d-none');
                sgramContainer.classList.remove('d-none');
            } else {
                audioContainer.classList.add('d-none');
                sgramContainer.classList.add('d-none');
            }
        }
        // Package audio file into form and send to server-side
        let fd = new FormData();
        fd.append("audio_data", audioBlob, "filename.webm");
        req.send(fd);
    });
    // Audio recorder on click event
    player.addEventListener('click', e => {
        const icon = document.querySelector('#record-icon');
        if (player.dataset.action == 'ready') {
            mediaRecorder.start();
            icon.classList.replace('oi-microphone', 'oi-media-record');
            icon.classList.remove('large-icon');
            player.dataset.action = 'recording';
            resetClock();
            clockFunction = window.setInterval(updateClock, 10);
        } else {
            mediaRecorder.stop();
            icon.classList.replace('oi-media-record', 'oi-microphone');
            player.dataset.action = 'ready';
            window.clearInterval(clockFunction);
        }
    })
});

function resetClock() {
    document.querySelector('#minutes').textContent = '00';
    document.querySelector('#seconds').textContent = '00';
    document.querySelector('#deciseconds').textContent = '00';
}
// Timer function to update clock
function updateClock() {
    minutesElement = document.querySelector('#minutes');
    secondsElement = document.querySelector('#seconds');
    decisecondsElement = document.querySelector('#deciseconds');

    deciseconds = parseInt(decisecondsElement.textContent) + 1;
    // Update time values
    if (deciseconds >= 100) {
        decisecondsElement.textContent = '00';
        secondsText = (parseInt(secondsElement.textContent) + 1).toString();
        if (secondsText.length < 2) secondsText = '0' + secondsText;
        secondsElement.textContent = secondsText;
        if (secondsElement.textContent >= 60) {
            secondsElement.textContent = '00';
            minutesText = (parseInt(minutesElement.textContent) + 1).toString();
            if (minutesText.length < 2) minutesText = '0' + minutesText;
            minutesElement.textContent = minutesText;
        }
    } else {
        decisecondsText = deciseconds.toString();
        if (decisecondsText.length < 2) decisecondsText = '0' + decisecondsText;
        decisecondsElement.textContent = decisecondsText;
    }
}
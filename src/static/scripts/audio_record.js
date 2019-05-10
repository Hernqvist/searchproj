const player = document.querySelector('#player');
 
navigator.mediaDevices.getUserMedia({ audio: true })
.then(stream => {
    mediaRecorder = new MediaRecorder(stream);
    let audioChunks = []

    mediaRecorder.addEventListener('dataavailable', e => {
        audioChunks.push(e.data);
    });
    mediaRecorder.addEventListener("stop", () => {
        const audioBlob = new Blob(audioChunks, {type: 'audio/webm;codecs=opus'});
        const req = new XMLHttpRequest;
        req.open('POST', '/audio-upload', true);
        req.onload = function() {
            audioChunks = [];
            songName = document.querySelector('#song-name');
            songName.textContent = req.response;
        }
        let fd = new FormData();
        fd.append("audio_data", audioBlob, "filename.webm");
        req.send(fd);
    });

    player.addEventListener('click', e => {
        const icon = document.querySelector('#record-icon');
        if (player.dataset.action == 'ready') {
            mediaRecorder.start();
            icon.classList.replace('oi-microphone', 'oi-media-record');
            icon.classList.remove('large-icon');
            player.dataset.action = 'recording';
        } else {
            mediaRecorder.stop();
            icon.classList.replace('oi-media-record', 'oi-microphone');
            player.dataset.action = 'ready';
        }
    })
});

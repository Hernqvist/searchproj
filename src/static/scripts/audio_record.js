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
            if (req.response.length > 200) {
                req.response = 'No Match';
            }
            audioChunks = [];
            songName = document.querySelector('#song-name');
            songName.textContent = req.response;
            const audioPlayer = document.querySelector('#song-player');
            if (req.response != 'No Match') {
                audioPlayer.src = '/static/dataset/' + encodeURI(req.response) + '.mp3';
                audioPlayer.classList.replace('d-none', 'd-block');
                audioPlayer.load();
            } else {
                audioPlayer.classList.replace('d-block', 'd-none');
            }
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

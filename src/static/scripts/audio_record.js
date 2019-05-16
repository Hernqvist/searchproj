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
            console.log(req.response)
            if (req.response.length > 100) {
                req.response = 'No Match';
            }
            audioChunks = [];
            songName = document.querySelector('#song-name');

            song = req.response.substring(0, req.response.search(';'));
            sgramFile = req.response.substring(req.response.search(';') + 1, req.response.length);
            songName.textContent = song;

            const audioContainer = document.querySelector('#audio-container');
            const sgramContainer = document.querySelector('#sgram-container');
            const audioPlayer = document.querySelector('#audio-player');
            const sgramImage = document.querySelector('#sgram-image');
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

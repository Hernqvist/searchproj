from flask import Flask, render_template,request, url_for, redirect
from pydub import AudioSegment
import io
import uuid
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('audio.html')

@app.route('/audio-upload', methods=['POST'])
def audio_upload():
    audioContent = request.files['audio_data'].read()
    webmAudio = AudioSegment.from_file(io.BytesIO(audioContent), format='webm', codec='opus')

    fileName = './audioFiles/' + uuid.uuid4().hex + '.wav'
    if not os.path.exists('./audioFiles/'):
        os.makedirs('./audioFiles')
    if not os.path.exists('./fpdbase.pklz'):
        return 'Dataset has not been indexed'

    webmAudio.export(fileName, format="wav")
    output = str(subprocess.check_output(['python3', 'audfprint.py', 'match', '--dbase', 'fpdbase.pklz', fileName, '--illustrate']))
    print(output)
    if (output.find('NOMATCH') != -1):
        return 'No Match'
    else:
        sIndex = output.find('dataset/') + 8
        eIndex = output.find('.mp3')
        return output[sIndex:eIndex]

if __name__ == '__main__':
    app.run(debug=True)
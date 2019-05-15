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

    fileName = './audioFiles/' + uuid.uuid4().hex + '.mp3'
    if not os.path.exists('./audioFiles/'):
        os.makedirs('./audioFiles')
    if not os.path.exists('./fpdbase.pklz'):
        return 'Dataset has not been indexed'
    webmAudio.export(fileName, format="mp3")

    tryOtherPitches = True

    if tryOtherPitches:
        output = str(subprocess.check_output(['python', 'audfprint.py', 'match_pitch', '--dbase', 'fpdbase.pklz', fileName, '--illustrate']))
        print(output)
        if (output.find('NOMATCH') != -1):
            return 'No Match'
        else:
            return output
    else:
        output = str(subprocess.check_output(['python', 'audfprint.py', 'match', '--dbase', 'fpdbase.pklz', fileName, '--illustrate']))
        print(output)
        if (output.find('NOMATCH') != -1):
            return 'No Match'
        else:
            sIndex = output.find('dataset/') + 8
            eIndex = output.find('.mp3')
            return output[sIndex:eIndex]

if __name__ == '__main__':
    app.run(debug=True)
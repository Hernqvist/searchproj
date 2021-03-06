from flask import Flask, render_template,request, url_for, redirect
from pydub import AudioSegment
import io
import uuid
import os
import subprocess

app = Flask(__name__)

# Home route
@app.route('/')
def index():
    return render_template('audio.html')

# Route for uploading and analyzing audio
@app.route('/audio-upload', methods=['POST'])
def audio_upload():
    # Read audio file
    audioContent = request.files['audio_data'].read()
    webmAudio = AudioSegment.from_file(io.BytesIO(audioContent), format='webm', codec='opus')
    # Check if data has been indexed
    fileName = './audioFiles/audio-regular.mp3'
    if not os.path.exists('./audioFiles/'):
        os.makedirs('./audioFiles')
    if not os.path.exists('./databases/database.pklz'):
        return 'Dataset has not been indexed;;'
    # Export audio
    webmAudio.export(fileName, format="mp3")

    tryOtherPitches = False

    # Delete sgram files
    sgramFile = ''
    for filename in os.listdir('./src/static'):
        if filename.startswith("sgram"): 
            os.remove('./src/static/' + filename)

    try:
        if tryOtherPitches:
            output = str(subprocess.check_output(['python3', 'audfprint.py', 'match_pitch', '--dbase', 'databases/database.pklz', fileName, '--illustrate']))
            print(output)
            if (output.find('NOMATCH') != -1):
                return 'No Match;;'
            else:
                return output + ';' + sgramFile
        else:
            # Run fingerprinting algorithm
            output = str(subprocess.check_output(['python3', 'audfprint.py', 'match', '--dbase', 'databases/database.pklz', fileName, '--illustrate']))
            # Create sgram image file
            for filename in os.listdir('./src/static'):
                if filename.startswith("sgram"): 
                    sgramFile = filename
            print(output)
            # Return match or no match to client side script
            if (output.find('NOMATCH') != -1):
                return 'No Match' + ';;'
            else:
                sIndex = output.find('songs/') + 6
                eIndex = output.find('.mp3', sIndex)
                return output[sIndex:eIndex] + ';' + sgramFile
    except:
        return 'No Match;;'

if __name__ == '__main__':
    app.run(debug=True)
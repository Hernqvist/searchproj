import librosa
import numpy as np
import matplotlib.pyplot as plt
import sys
from pydub import AudioSegment

class AudioAugmentation:
    def read_audio_file(self, filename):
        if filename.endswith(".mp3"):
            # convert to wav
            sound = AudioSegment.from_mp3(filename)
            sound.export("tmp.wav", format="wav")
            # make mono channel music
            sound = AudioSegment.from_wav("tmp.wav")
            sound = sound.set_channels(1)
            sound.export("tmp.wav", format="wav")
            filename="tmp.wav"
        # use None sampling rate to preserve the original one
        data, sr = librosa.core.load(filename, sr=None)
        return data, sr

    def write_audio_file(self, file, data, sample_rate=16000):
        librosa.output.write_wav(file, data, sample_rate)

    def plot_time_series(self, data):
        fig = plt.figure(figsize=(14, 8))
        plt.title('Raw wave ')
        plt.ylabel('Amplitude')
        plt.plot(np.linspace(0, 1, len(data)), data)
        plt.show()

    def add_noise(self, data, sigma=0.005):
        noise = np.random.randn(len(data))
        data_noise = data + sigma * noise
        return data_noise

    def shift(self, data):
        return np.roll(data, 1600)

    def stretch(self, data, rate=1):
        data = librosa.effects.time_stretch(data, rate)
        return data

# Create a new instance from AudioAugmentation class
aa = AudioAugmentation()

# Read and show cat sound
data, sr = aa.read_audio_file(sys.argv[1])

# Adding noise to sound
orig_data = np.copy(data)
data_noise = aa.add_noise(data, sigma=0.0)
print("MSE", np.sum(np.sqrt(np.square(orig_data - data_noise))))

# Write generated cat sounds
aa.write_audio_file('output/generated_cat1.wav', data_noise, sample_rate=sr)

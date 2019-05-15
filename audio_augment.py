import librosa
import numpy as np
# import matplotlib.pyplot as plt
import sys
from pydub import AudioSegment
# import soundfile as sf

class AudioAugmentation:
    def read(self, f, start_index=0, end_index=-1):
        """MP3 to numpy array"""
        a = AudioSegment.from_mp3(f)
        sample = a[start_index:end_index]
        y = np.array(sample.get_array_of_samples())
        if sample.channels == 2:
            y = y.reshape((-1, 2))
        return sample.frame_rate, y

    def write(self, f, sr, x, normalized=False):
        """numpy array to MP3"""
        channels = 2 if (x.ndim == 2 and x.shape[1] == 2) else 1
        if normalized:  # normalized array - each item should be a float in [-1, 1)
            y = np.int16(x * 2 ** 15)
        else:
            y = np.int16(x)
        song = AudioSegment(y.tobytes(), frame_rate=sr, sample_width=2, channels=channels)
        song.export(f, format="mp3", bitrate="320k")

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
        # sf.write(file, data, sample_rate, format=file_format)

    # def plot_time_series(self, data):
    #     fig = plt.figure(figsize=(14, 8))
    #     plt.title('Raw wave ')
    #     plt.ylabel('Amplitude')
    #     plt.plot(np.linspace(0, 1, len(data)), data)
    #     plt.show()

    def add_noise(self, data, sigma=0.005):
        noise = np.random.normal(0, sigma, size=data.shape)
        data_noise = data + noise
        return data_noise

    def pitch_shift(self, sample, octaves=0.0):
        new_sr = int(sample.frame_rate * (2.0 ** octaves))
        shifted = sample._spawn(sample.raw_data, overrides={'frame_rate': new_sr})
        return shifted, new_sr

    def shift(self, data):
        return np.roll(data, 1600)

    def stretch(self, data, rate=1):
        data = librosa.effects.time_stretch(data, rate)
        return data

# # Create a new instance from AudioAugmentation class
# aa = AudioAugmentation()

# # Read and show cat sound
# data, sr = aa.read_audio_file(sys.argv[1])

# # Adding noise to sound
# orig_data = np.copy(data)
# data_noise = aa.add_noise(data, sigma=0.0)
# print("MSE", np.sum(np.sqrt(np.square(orig_data - data_noise))))

# # Write generated cat sounds
# aa.write_audio_file('output/generated_cat1.wav', data_noise, sample_rate=sr)

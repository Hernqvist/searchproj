from audio_augment import AudioAugmentation
import sys

def main(file, sigma):
    aa = AudioAugmentation()
    
    sr, sample = aa.read(file) # read sample
    noisy_sample = aa.add_noise(sample, sigma) # apply gaussian noise
    aa.write("output_{}.mp3".format(int(sigma)), sr, noisy_sample)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 audio_noise_creator <music_file> <sigma>")
    main(file=sys.argv[1], sigma=float(sys.argv[2]))
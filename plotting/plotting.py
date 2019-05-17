from matplotlib import rc
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from audfprint_analyze import Analyzer
import sys

def plot_spectrogram(filename):
    a = Analyzer()
    peaks, sgram = a.wavfile2peaks(filename, return_spectrogram=True)

    sgram = 20.0 * np.log10(np.maximum(sgram, np.max(sgram) / 1e6))

    x_coords = [x for (x,y) in peaks]
    y_coords = [y for (x,y) in peaks]

    # target sampling rate of audfprint
    sr = 11025

    fig, ax = plt.subplots(figsize=(6,6))
    s = np.max(sgram) - sgram
    ax.imshow(s, aspect=1.7, cmap="gray", origin="lower")

    ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x//43.06640625))
    ax.xaxis.set_major_formatter(ticks_x)
    ticks_y = ticker.FuncFormatter(lambda y, pos: '{0:g}'.format(int(y*21.533203125)))
    ax.yaxis.set_major_formatter(ticks_y)

    y_ticks_to_plot = [0,500,1000,1500,2000,2500,3000,3500,4000]
    plt.yticks(np.array(y_ticks_to_plot)/21.533203125, labels=y_ticks_to_plot)
    ax.set_ylim(0,190)
    ax.set_xlim(1300,1750)
    ax.set_ylabel('Frequency [Hz]')
    ax.set_xlabel('Time [sec]')
    plt.savefig("spectogram.png", bbox_inches="tight")
    plt.show()

    fig, ax = plt.subplots(figsize=(6,6))
    s = np.max(sgram) - sgram
    ax.imshow(s, aspect=1.7, cmap="gray", origin="lower")
    ax.scatter(x_coords,y_coords,marker="x", color="white")

    ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x//43.06640625))
    ax.xaxis.set_major_formatter(ticks_x)
    ticks_y = ticker.FuncFormatter(lambda y, pos: '{0:g}'.format(int(y*21.533203125)))
    ax.yaxis.set_major_formatter(ticks_y)

    y_ticks_to_plot = [0,500,1000,1500,2000,2500,3000,3500,4000]
    plt.yticks(np.array(y_ticks_to_plot)/21.533203125, labels=y_ticks_to_plot)
    ax.set_ylim(0,190)
    ax.set_xlim(1300,1750)
    ax.set_ylabel('Frequency [Hz]')
    ax.set_xlabel('Time [sec]')
    plt.savefig("spectogram_scatter.png", bbox_inches="tight")
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 plotting.py <music_file_name>")
    plot_spectrogram(sys.argv[1])
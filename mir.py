import sklearn
import scipy
from scipy.io import wavfile
import pyaudio
import numpy as np
import time
import wave
import os
from matplotlib import pyplot as plt
from matplotlib import style
import struct
from numpy import fft
from scipy import fftpack
import threading
from queue import Queue


style.use('ggplot')

# TODO: Thread this - https://www.youtube.com/watch?v=NwH0HvMI4EA
# TODO: Install essentia - http://essentia.upf.edu/documentation/installing.html
# TODO: Fourier Transform - https://docs.scipy.org/doc/numpy/reference/generated/numpy.fft.fft.html
# TODO: MIR - https://www.youtube.com/watch?v=oGGVvTgHMHw&list=WL&index=393


def main():
    file = 'D:\\Programming\\Python (Py)\\OYE\\Audio\\Drumloops\\vinyl_dl_135.wav'
    with wave.open(file, 'rb') as loop:
        play_audio(loop)
    plot_wave(file)


def plot_wave(file):
    samples = wavfile.read(file)[1]
    plt.plot(np.arange(len(samples)), samples)
    plt.xlabel('Time - Sample Number')
    plt.ylabel('Amplitude')
    plt.show()


def play_audio(file):
    """ Plays a single audio file """
    chunk = 1024
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(file.getsampwidth()),
                    channels=file.getnchannels(),
                    rate=file.getframerate(),
                    output=True)

    data = file.readframes(chunk)
    while data != '':
        stream.write(data)
        data = file.readframes(chunk)

    stream.close()
    p.terminate()


def play_files(directory, amount=99999):
    """ Plays all of the files from a directory.
     You can specify the number of files to play by modifying the amount:parameter """
    files = os.listdir(directory)

    for file in files:
        with wave.open(directory + file, 'rb') as sound:
            play_audio(sound)
        if amount <= 1:
            return
        amount -= 1


def enumerate_files(directory):
    """ Names all files in a directory from 0 with a .wav extension """
    files = os.listdir(directory)
    i = 0

    for file in files:
        os.rename(os.path.join(directory, file), os.path.join(directory, str(i) + '.wav'))
        i += 1

if __name__ == "__main__":
    main()

import wave, os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
import scipy.interpolate as interp

np.set_printoptions(threshold=np.nan)

def process_file(directory, file_name):

    wf = wave.open(directory + "/" + file_name)
    wf_framerate = wf.getframerate()
    wf.close()

    audio_data = read(directory + "/" + file_name)
    audio_matrix_ref = np.zeros(1024)
    audio_matrix = np.array(audio_data[1], dtype=np.int16)
    audio_matrix_interp = interp.interp1d(np.arange(audio_matrix.size), audio_matrix)
    audio_matrix_interp_ref = audio_matrix_interp(np.linspace(0, audio_matrix.size - 1, audio_matrix_ref.size))
    print str(len(audio_matrix_interp_ref))

    # pcm data
    # plt.plot(audio_matrix_interp_ref.flatten())
    # plt.show()

    fft_stores = []
    freq_stores = []
    max_fft_amplitude = 0
    for x in range(32):
        sub = audio_matrix_interp_ref[x * 32 : x * 32 + 32]

        fft = np.abs(np.fft.fft(sub.flatten() * np.blackman(32)))
        freq = np.fft.fftfreq(32, 1.0 / 32.0)

        fft = fft[4 : int(len(fft)/2)]
        freq = freq[4 : int(len(freq)/2)]

        fft_stores.append(fft)
        freq_stores.append(freq)

        fft_rev = fft[::-1]
        i_max = np.argmax(fft_rev)

        if fft_rev[i_max] > max_fft_amplitude: max_fft_amplitude = fft_rev[i_max]

    perc_stores = np.zeros((32, 32))
    for x in range(32):
        for y in range(12):
            perc_stores[x][y] = fft_stores[x][y] / max_fft_amplitude

    np.savetxt(directory + "/arr/" + file_name + ".txt", perc_stores)

if __name__ == "__main__":
    outputs = []
    dirs = os.listdir("train")
    for file_name in dirs:
        if ".wav" not in file_name:
            continue

        if "no" in file_name:
            outputs.append(0)
        else:
            outputs.append(1)

        process_file("train", file_name)

    outputs_arr = np.array(outputs)
    np.savetxt("train/outputs.txt", outputs_arr)

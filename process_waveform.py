import numpy as np
import scipy.interpolate as interp
import matplotlib.pyplot as plt

def process_waveform(audio_data):
    audio_matrix_ref = np.zeros(1024)
    audio_matrix = np.array(audio_data, dtype=np.int16)
    audio_matrix_interp = interp.interp1d(np.arange(audio_matrix.size), audio_matrix)
    audio_matrix_interp_ref = audio_matrix_interp(np.linspace(0, audio_matrix.size - 1, audio_matrix_ref.size))
    print(str(len(audio_matrix_interp_ref)))

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

    return perc_stores

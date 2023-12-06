#https://github.com/sigmf/SigMF/issues/114
from copy import deepcopy
import json
import numpy as np
import matplotlib.pyplot as plt

def naive_watermark(samples: np.memmap) -> np.memmap:
    # Extract the real and imaginary parts of the complex data
    real_part = np.real(samples)
    imaginary_part = np.imag(samples)

    watermarked = deepcopy(samples)

    return watermarked

def adjust_avg(samples, target: np.float64):
    delta = np.average(samples) - target
    length = len(samples)
    print(length)
    print(delta / length)
    while np.average(samples) > target:
        #print(f"Remaining: {np.average(samples) - target}")
        samples -= 1000 * np.float64(delta) / length
    #for i in range(0, length):
    #    samples[i] += np.float64(delta) / np.float64(length)


if __name__ == "__main__":
    # Grab the metadata file
    with open("data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#1_run1.sigmf-meta", "r") as f:
        md = json.loads(f.read())


    samples = []
    if md["_metadata"]["global"]["core:datatype"] == "cf32":
        samples = np.memmap("data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#1_run1.sigmf-data", mode="r", dtype=np.complex128)
    else:
        print("Unexpected data type!")
        exit()

    # Extract the real and imaginary parts of the complex data
    real_part = np.real(samples)
    imaginary_part = np.imag(samples)

    real_part = deepcopy(real_part)
    imaginary_part = deepcopy(imaginary_part)

    # Gathering some info
    real_avg = np.average(real_part)
    imag_avg = np.average(imaginary_part)

    print(f"Averages, Real: {real_avg}, Imaginary: {imag_avg}")
    
    adjust_avg(real_part, np.float64(-0.001))
    adjust_avg(imaginary_part, np.float64(-0.001))

    real_avg = np.average(real_part)
    imag_avg = np.average(imaginary_part)

    print(f"Averages, Real: {real_avg}, Imaginary: {imag_avg}")
    exit(1)


	# Create a figure and two subplots for real and imaginary parts
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

	# Plot the real part
    ax1.plot(real_part, label='Real Part', color='blue')
    ax1.set_title('Real Part')
    ax1.set_xlabel('Index')
    ax1.set_ylabel('Value')

	# Plot the imaginary part
    ax2.plot(imaginary_part, label='Imaginary Part', color='red')
    ax2.set_title('Imaginary Part')
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Value')

	# Show the plots
    plt.tight_layout()
    plt.show()

	# Playing around with FFT...
    Fs = float(md["_metadata"]["global"]["core:sample_rate"])
    N = len(samples)
    S = np.fft.fftshift(np.fft.fft(samples))
    S_mag = np.abs(S)
    S_phase = np.angle(S)
    f = np.arange(Fs/-2, Fs/2, Fs/N)
    plt.figure(0)
    plt.plot(f, S_mag,'.-')
    plt.figure(1)
    plt.plot(f, S_phase,'.-')
    plt.show()

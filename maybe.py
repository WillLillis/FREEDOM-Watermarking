#https://github.com/sigmf/SigMF/issues/114
import json
import numpy as np
import matplotlib.pyplot as plt

with open("data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#1_run1.sigmf-meta", "r") as f:
    md = json.loads(f.read())
print(type(md))
#print(md)
#if md["data_file"]["global"]["dtype"] == "cf32_le":
samples = []
if md["_metadata"]["global"]["core:datatype"] == "cf32":
    #samples = np.memmap("myrecord.sigmf-data", mode="r", dtype=np.complex64)
    samples = np.memmap("data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#1_run1.sigmf-data", mode="r", dtype=np.complex128)
    print(type(samples))
    print(samples)
elif md["_metadata"]["global"]["core:datatype"] == "ci16":
    samples = np.memmap("data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#1_run1.sigmf-data", mode="r", dtype=np.int16)

# Extract the real and imaginary parts of the complex data
real_part = np.real(samples)
imaginary_part = np.imag(samples)

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

# Playing around with FFT
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

#https://github.com/sigmf/SigMF/issues/114
from copy import deepcopy
import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

class constants:
    SAMPLE_META_DATA_PATH = "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#1_run1.sigmf-meta"
    SAMPLE_DATA_PATH = "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#1_run1.sigmf-data"
    APPLY_WATERMARK = 0
    EXTRACT_WATERMARK = 1

    WATERMARK_SINGLE_POINT = 0
    WATERMARK_SHIFT_AVG = 1
    WATERMARK_EXP = 2
    WATERMARK_TYPE = WATERMARK_SINGLE_POINT

    WATERMARK_POINT_IDX = 42
    WATERMARK_POINT_VAL_REAL = 0.5
    WATERMARK_POINT_VAL_IMAG = 0.5j

def data_stats(samples):
    pass

def plot_samples(samples):
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
    

def load_KRI_samples(meta_data_path=constants.SAMPLE_META_DATA_PATH, data_path=constants.SAMPLE_DATA_PATH):
    meta_data = {}
    with open(meta_data_path, "r") as f:
       meta_data = json.loads(f.read())

    samples = []
    if meta_data["_metadata"]["global"]["core:datatype"] == "cf32":
        samples = np.memmap(data_path, mode="r", dtype=np.complex128)
    else:
        print("Unexpected data type!")
        exit()

    return samples

def load_watermarked(data_path="watermarked_test.npy"):
    data = []
    with open(data_path, "rb") as f:
        data = np.load(f)
    return data


def write_samples(samples):
    #filename = f"watermarked_{datetime.now()}"
    filename = "watermarked_test"
    np.save(filename, samples)

def watermark_single_point(samples):
    val = constants.WATERMARK_POINT_VAL_REAL + constants.WATERMARK_POINT_VAL_IMAG
    print(f"Samples length: {len(samples)}")
    print(f"Before: Samples[{constants.WATERMARK_POINT_IDX}] = {samples[constants.WATERMARK_POINT_IDX]}")
    samples[constants.WATERMARK_POINT_IDX] = val
    print(f"After: Samples[{constants.WATERMARK_POINT_IDX}] = {samples[constants.WATERMARK_POINT_IDX]}")
    
def extract_watermark_single_point(samples):
    check_val = constants.WATERMARK_POINT_VAL_REAL + constants.WATERMARK_POINT_VAL_IMAG
    return samples[constants.WATERMARK_POINT_IDX] == check_val

def watermark_shift_avg(samples):
    pass

def extract_watermark_shift_avg(samples):
    pass

def watermark_exp(samples):
    pass

def extract_watermark_exp(samples):
    pass


def watermark_samples(samples):
    watermarked = deepcopy(samples)
    match constants.WATERMARK_TYPE:
        case constants.WATERMARK_SINGLE_POINT:
            watermark_single_point(watermarked)
        case constants.WATERMARK_SHIFT_AVG:
            watermark_shift_avg(watermarked)
        case constants.WATERMARK_EXP:
            watermark_exp(watermarked)

    return watermarked
    

def check_watermark(samples):
    is_watermarked = False
    match constants.WATERMARK_TYPE:
        case constants.WATERMARK_SINGLE_POINT:
            is_watermarked = extract_watermark_single_point(samples)
        case constants.WATERMARK_SHIFT_AVG:
            is_watermarked = extract_watermark_shift_avg(samples)
        case constants.WATERMARK_EXP:
            is_watermarked = extract_watermark_exp(samples)

    return is_watermarked


if __name__ == "__main__":
    choice = int(input("Select:\n\t0: Watermark Sample Data\n\t1: Test Data for Watermark\n"))
    print(f"Choice: {choice}")

    watermarked = []
    is_watermarked = False
    match choice:
        case constants.APPLY_WATERMARK:
            data = load_KRI_samples()
            print("Watermarking data...")
            watermarked = watermark_samples(data)
            print("Writing watermarked data to disk...")
            write_samples(watermarked)
            print("done!")
        case constants.EXTRACT_WATERMARK:
            print("Extracting watermark...")
            watermarked_data = load_watermarked(data_path="watermarked_test.npy")
            print("Watermarked data:")
            plot_samples(watermarked_data)
            is_watermarked = check_watermark(watermarked_data)
            print(f"Marked data, Watermark Detected: {is_watermarked}")
            clean_data = load_KRI_samples()
            print("Clean data:")
            plot_samples(clean_data)
            is_watermarked = check_watermark(clean_data)
            print(f"Clean data, Watermark Detected: {is_watermarked}")

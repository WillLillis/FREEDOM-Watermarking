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
    TEST_WATERMARK = 2

    WATERMARK_SINGLE_POINT = 0
    WATERMARK_SHIFT_AVG = 1
    WATERMARK_EXP = 2
    WATERMARK_TYPE = WATERMARK_SHIFT_AVG

    WATERMARK_POINT_IDX = 42
    WATERMARK_POINT_VAL_REAL = 0.5
    WATERMARK_POINT_VAL_IMAG = 0.5j
    WATERMARK_POINT_VAL = WATERMARK_POINT_VAL_REAL + WATERMARK_POINT_VAL_IMAG

    WATERMARK_AVG_VAL_REAL = -0.001
    WATERMARK_AVG_VAL_IMAG = -0.001j
    WATERMARK_AVG_VAL = WATERMARK_AVG_VAL_REAL + WATERMARK_AVG_VAL_IMAG
    WATERMARK_AVG_SCALE = 1000.0

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
    check_val = constants.WATERMARK_POINT_VAL
    return samples[constants.WATERMARK_POINT_IDX] == check_val

def watermark_shift_avg(samples, target=constants.WATERMARK_AVG_VAL):
    delta = np.absolute(np.average(samples) - target)
    length = len(samples)
    while np.average(samples) > target:
        #print(f"Remaining: {np.average(samples) - target}")
        adj_val = constants.WATERMARK_AVG_SCALE * delta / length
        samples -= complex(adj_val, adj_val)

def extract_watermark_shift_avg(samples, target=constants.WATERMARK_AVG_VAL):
    #print(f"Average: {np.average(samples)}")
    if np.average(samples) <= target:
        return True
    else:
        return False

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

def add_gaussian_noise(samples, strength=0.00025):
    rands = np.random.normal(0.0, 1.0, len(samples)) * strength
    val = [complex(num, num) for num in rands]
    samples += val

def test_extraction(samples, noise_strength, n_trials=100):
    n_correct = 0
    for i in range(0, n_trials):
        #print(f"\t\t{i}")
        if i % 20 == 0:
            print(f"\t\t{i}")
        #print(f"Before watermark: {np.average(samples)}")
        tmp = watermark_samples(samples)
        #print("Watermarked samples")
        #print(f"After watermark: {np.average(tmp)}")
        add_gaussian_noise(tmp, strength=noise_strength)
        #print("Added noise")
        #print(f"After noise: {np.average(tmp)}")
        if check_watermark(tmp):
            #print(f"{i}: Success!")
            n_correct += 1
        else:
            pass
            #print(f"{i}: Failure :(")
    print(f"\t\t{n_correct} out of {n_trials}: {n_correct / n_trials}")


def test_stuff():
    metadata_files = ["data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#1_run1.sigmf-meta", 
                      "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#2_run1.sigmf-meta",
                      "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#3_run1.sigmf-meta", # entire process hangs...
                      "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#4_run1.sigmf-meta",
                      "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#5_run1.sigmf-meta",
                      "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#7_run1.sigmf-meta",
                      "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#9_run1.sigmf-meta",
                      "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#13_run1.sigmf-meta",
                      "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#14_run1.sigmf-meta",
                      "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#15_run1.sigmf-meta",
                      "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#17_run1.sigmf-meta",
                      "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#18_run1.sigmf-meta",
                      "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#19_run1.sigmf-meta",
                      "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#25_run1.sigmf-meta",
                      "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#26_run1.sigmf-meta"]

    data_files = ["data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#1_run1.sigmf-data",
                  "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#2_run1.sigmf-data",
                  "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#3_run1.sigmf-data",
                  "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#4_run1.sigmf-data",
                  "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#5_run1.sigmf-data",
                  "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#7_run1.sigmf-data",
                  "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#9_run1.sigmf-data",
                  "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#13_run1.sigmf-data",
                  "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#14_run1.sigmf-data",
                  "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#15_run1.sigmf-data",
                  "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#17_run1.sigmf-data",
                  "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#18_run1.sigmf-data",
                  "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#19_run1.sigmf-data",
                  "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#25_run1.sigmf-data",
                  "data/KRI-16IQImbalances-DemodulatedData/Demod_WiFi_cable_X310_3123D76_IQ#26_run1.sigmf-data"]
    
    noise_strengths = [0.01, 0.001, 0.0007, 0.0005, 0.00025, 0.0001, 0.00001]

    #dataset_num = 2
    for strength in range(0, len(noise_strengths)):
        print(f"Strength: {noise_strengths[strength]}")
        for dataset_num in range(0,len(data_files)):
            print(f"\tDataset {dataset_num}")
            data = load_KRI_samples(metadata_files[dataset_num], data_files[dataset_num])
            test_extraction(data, noise_strengths[strength])

if __name__ == "__main__":
    test_stuff()
    exit(0)
    
    choice = int(input("Select:\n\t0: Watermark Sample Data\n\t1: Test Data for Watermark\n\t2: Test Watermark with Noise\n"))
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
        case constants.TEST_WATERMARK:
            print("Testing watermarking...")
            data = load_KRI_samples()
            test_extraction(data)

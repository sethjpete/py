import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.integrate import simpson

def generate_reddit_progress_bar(percentage : float, out_len = 10) -> str:
    assert 0 <= percentage <= 1, "Percentage must be between 0 and 1"
    completed_char = "🔵"
    incomplete_char = "⚪️"
    num_convolutions = 3
    magic_number = int((percentage * 100) / (num_convolutions / 2))
    if magic_number == 0:
        return incomplete_char * out_len
    # generate and convolve two random uniform distributions
    x = np.random.uniform(0,10, size = magic_number)
    y = np.random.uniform(0,10, size = magic_number)
    z = np.random.uniform(0,10, size = magic_number)
    distribution = np.convolve(x,y)
    distribution = np.convolve(distribution,z)
    # scale the distribution so that the area under the curve is 1
    distribution = distribution / np.sum(distribution)
    # convolve the distribution with the copy vector
    # take 10 samples from the distribution and average them
    avg = 0
    for i in range(10):
        avg += np.random.choice(np.arange(1, len(distribution) + 1), p=distribution)
    avg /= 10
    num_completed = min(int(avg/100 * out_len),out_len)
    return num_completed * completed_char + (out_len-num_completed) * incomplete_char

def main():
    print("WORKING.....")
    for i in range(1,101):
        print(generate_reddit_progress_bar(i/100), end="\r")
        time.sleep(0.1)
    print("🔵"*10)
    print("DONE!")

if __name__ == "__main__":
    main()

import tkinter as tk
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import cv2

def plot_graphs():
    # Read the image
    img = cv2.imread(entry_image_path.get())
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB for displaying with matplotlib

    # Display the original image
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    axes[0].imshow(img)
    axes[0].set_title('Original Image', fontsize=10)
    axes[0].axis('off')

    # Convert the image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Extract input values
    samp_freq = float(entry_samp_freq.get())  # Sample frequency (Hz)
    notch_freq = float(entry_notch_freq.get())  # Frequency to be removed from signal (Hz)
    quality_factor_percentage = float(entry_quality_factor.get())  # Quality factor (%)

    # Convert quality factor from percentage to decimal
    quality_factor = quality_factor_percentage / 100.0

    # Design a notch filter using signal.iirnotch
    b_notch, a_notch = signal.iirnotch(notch_freq, quality_factor, samp_freq)

    # Apply notch filter to the grayscale image using signal.filtfilt
    output_img = signal.filtfilt(b_notch, a_notch, gray_img)

    # Display the denoised image
    axes[1].imshow(output_img, cmap='gray')
    axes[1].set_title('Denoised Image', fontsize=10)
    axes[1].axis('off')

    # Compute magnitude response of the designed filter
    freq, h = signal.freqz(b_notch, a_notch, fs=samp_freq)

    # Plot magnitude response of the filter
    axes[2].plot(freq * samp_freq / (2 * np.pi), 20 * np.log10(abs(h)),
                 'r', label='Bandpass filter', linewidth='2')
    axes[2].set_xlabel('Frequency [Hz]', fontsize=8)
    axes[2].set_ylabel('Magnitude [dB]', fontsize=8)
    axes[2].set_title('Notch Filter Magnitude Response', fontsize=8)
    axes[2].grid()

    plt.tight_layout()
    plt.show()

# Create tkinter window
root = tk.Tk()
root.title("Image Denoising")

# Labels
tk.Label(root, text="Image Path:").grid(row=0, column=0, padx=5, pady=5)
tk.Label(root, text="Sample Frequency (Hz):").grid(row=1, column=0, padx=5, pady=5)
tk.Label(root, text="Notch Frequency (Hz):").grid(row=2, column=0, padx=5, pady=5)
tk.Label(root, text="Quality Factor (%):").grid(row=3, column=0, padx=5, pady=5)

# Entry fields
entry_image_path = tk.Entry(root)
entry_image_path.grid(row=0, column=1, padx=5, pady=5)
entry_image_path.insert(0, "path_to_your_image.jpg")

entry_samp_freq = tk.Entry(root)
entry_samp_freq.grid(row=1, column=1, padx=5, pady=5)
entry_samp_freq.insert(0, "1000")

entry_notch_freq = tk.Entry(root)
entry_notch_freq.grid(row=2, column=1, padx=5, pady=5)
entry_notch_freq.insert(0, "50")

entry_quality_factor = tk.Entry(root)
entry_quality_factor.grid(row=3, column=1, padx=5, pady=5)
entry_quality_factor.insert(0, "20")

# Button
button_plot = tk.Button(root, text="Result", command=plot_graphs)
button_plot.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()

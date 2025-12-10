import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Synthetic EEG parameters
# ----------------------------
fs = 250            # sampling rate (Hz)
T = 10.0            # duration (seconds)
t = np.arange(0, T, 1/fs)

rng = np.random.default_rng(0)  # for reproducibility

def simulate_eeg(alpha_amp, beta_amp, noise_sd):
    """Generate synthetic EEG as alpha + beta + Gaussian noise."""
    alpha = alpha_amp * np.sin(2 * np.pi * 10 * t)   # 10 Hz alpha
    beta = beta_amp * np.sin(2 * np.pi * 20 * t)     # 20 Hz beta
    noise = noise_sd * rng.standard_normal(len(t))
    return alpha + beta + noise

# Rest: strong alpha, little beta
rest = simulate_eeg(alpha_amp=20, beta_amp=2, noise_sd=5)

# Task: reduced alpha, stronger beta (alpha "suppression")
task = simulate_eeg(alpha_amp=8, beta_amp=10, noise_sd=5)

def compute_psd(signal, fs):
    """Compute power spectrum via single-sided FFT."""
    n = len(signal)
    window = np.hanning(n)
    sig_win = signal * window
    freqs = np.fft.rfftfreq(n, d=1/fs)
    fft_vals = np.fft.rfft(sig_win)
    psd = (np.abs(fft_vals) ** 2) / (fs * np.sum(window**2))
    return freqs, psd

freqs, psd_rest = compute_psd(rest, fs)
_, psd_task = compute_psd(task, fs)

# ----------------------------
# Band power calculation
# ----------------------------
alpha_band = (8, 12)
beta_band = (13, 30)

def band_power(freqs, psd, band):
    idx = (freqs >= band[0]) & (freqs <= band[1])
    return np.trapz(psd[idx], freqs[idx])

alpha_rest = band_power(freqs, psd_rest, alpha_band)
alpha_task = band_power(freqs, psd_task, alpha_band)
beta_rest  = band_power(freqs, psd_rest, beta_band)
beta_task  = band_power(freqs, psd_task, beta_band)

print("Alpha power  - Rest:", alpha_rest, " Task:", alpha_task)
print("Beta  power  - Rest:", beta_rest,  " Task:", beta_task)

# ----------------------------
# Plot 1: time-domain snippet
# ----------------------------
mask = t < 2.0  # first 2 seconds
plt.figure(figsize=(8, 4))
plt.plot(t[mask], rest[mask], label="Rest")
plt.plot(t[mask], task[mask], label="Task", alpha=0.7)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (µV)")
plt.title("Synthetic EEG (first 2 s)")
plt.legend()
plt.tight_layout()

# ----------------------------
# Plot 2: power spectra
# ----------------------------
plt.figure(figsize=(8, 4))
plt.semilogy(freqs, psd_rest, label="Rest")
plt.semilogy(freqs, psd_task, label="Task")
plt.xlim(0, 40)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Power (a.u., log scale)")
plt.title("Power Spectrum of Synthetic EEG")
plt.legend()
plt.tight_layout()

# ----------------------------
# Plot 3: band power bar chart
# ----------------------------
labels = ["Alpha (8–12 Hz)", "Beta (13–30 Hz)"]
rest_vals = [alpha_rest, beta_rest]
task_vals = [alpha_task, beta_task]

x = np.arange(len(labels))
w = 0.35

plt.figure(figsize=(6, 4))
plt.bar(x - w/2, rest_vals, width=w, label="Rest")
plt.bar(x + w/2, task_vals, width=w, label="Task")
plt.xticks(x, labels)
plt.ylabel("Band Power (a.u.)")
plt.title("Band Power by Condition")
plt.legend()
plt.tight_layout()

plt.show()

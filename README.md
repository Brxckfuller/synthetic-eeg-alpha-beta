# Synthetic EEG: Alpha Suppression & Beta Enhancement

This project simulates EEG signals under **Rest** and **Task** conditions using controlled alpha (10 Hz) and beta (20 Hz) oscillations plus Gaussian noise. It reproduces a classic neural pattern: **reduced alpha and increased beta power during cognitive engagement**.

## Methods

- Generate synthetic EEG:
  - Rest: strong 10 Hz alpha, weak 20 Hz beta + Gaussian noise
  - Task: reduced alpha, stronger beta + Gaussian noise
- Sampling rate: 250 Hz, 10 s duration
- Power spectral density (PSD) via single-sided FFT
- Band-power integration:
  - Alpha: 8–12 Hz
  - Beta: 13–30 Hz

## Outputs

The script produces three main visualisations:

1. **Time-series snippet (first 2 s)**  
   Rest shows a clearer 10 Hz rhythm; Task includes additional faster activity.

2. **Power spectrum (0–40 Hz, log power)**  
   - Rest: dominant alpha peak around 10 Hz  
   - Task: reduced alpha and stronger beta peak around 20 Hz  

3. **Band-power bar chart**  
   - Alpha power: Rest >> Task (alpha suppression)  
   - Beta power: Task >> Rest (task-related beta enhancement)  

## Tools

- Python 3
- NumPy
- Matplotlib

No real EEG data are required – everything is simulated, making it fully shareable and reproducible.


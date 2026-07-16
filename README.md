```
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⢀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣤⣶⣿⣿⣿⣆⠘⠿⠟⢻⣿⣿⡇⢐⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢸⣿⣿⣿⣧⡄⠙⣿⣷⣶⣶⡿⠿⠿⢃⣼⡟⠻⣿⣿⣶⡄⠀⠀⠀⠀
⠀⠀⢰⣷⣌⠙⠉⣿⣿⡟⢀⣿⣿⡟⢁⣤⣤⣶⣾⣿⡇⠸⢿⣿⠿⢃⣴⡄⠀⠀
⠀⠀⢸⣿⣿⣿⣿⠿⠋⣠⣾⣿⣿⠀⣾⣿⣿⣛⠛⢿⣿⣶⣤⣤⣴⣿⣿⣿⡆⠀
⠀⣴⣤⣄⣀⣠⣤⣴⣾⣿⣿⣿⣿⣆⠘⠿⣿⣿⣷⡄⢹⣿⣿⠿⠟⢿⣿⣿⣿⠀
⠀⢸⣿⣿⡿⠛⠛⣻⣿⣿⣿⣿⣿⣿⣷⣦⣼⣿⣿⠃⣸⣿⠃⢰⣶⣾⣿⣿⡟⠀
⠀⠀⢿⡏⢠⣾⣿⣿⡿⠋⣠⣄⡉⢻⣿⣿⡿⠟⠁⠀⠛⠛⠀⠘⠿⠿⠿⠋⠀⠀
⠀⠀⠀⠁⠘⢿⣿⣿⣷⣤⣿⣿⠗⠀⣉⣥⣴⣶⡶⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣤⣀⡉⠛⠛⠋⣉⣠⣴⠿⢿⣿⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠻⢿⣿⣿⣿⣿⡿⠋⣠⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⡾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

```
# Kuramoto Oscillator Model

**Computational Neuroscience • Dynamical Systems**

A computational neuroscience project that simulates a network of coupled Kuramoto phase oscillators and compares the resulting synthetic EEG power spectrum against real EEG recordings from the **BCI Competition IV Dataset 2b**.

The objective is to investigate whether a simple synchronization model can reproduce the dominant alpha-band oscillation observed in human EEG.

---

## Overview

Neural populations often exhibit synchronized oscillatory activity. The Kuramoto model is one of the simplest mathematical frameworks for studying synchronization in coupled oscillatory systems.

This project implements a network of Kuramoto oscillators, generates a synthetic EEG-like signal, computes its power spectral density (PSD), and quantitatively compares it with experimental EEG recordings.

Unlike many demonstrations that compare against a single recording, this implementation validates the model using **all 45 recordings** available in the BCI Competition IV Dataset 2b.

---

## Results

<p align="center">
  <img src="output/log scale plots/average_eeg.png" width="900">
</p>

<p align="center">
Average EEG Spectrum (Using Logarithmic Y-axis Scale)
</p>

<p align="center">
  <img src="output/linear scale plots/final_average_comparison.png" width="900">
</p>

<p align="center">
Comparison between the synthetic Kuramoto spectrum and the average EEG spectrum across all 45 recordings  (Using Linear Y-axis Scale)
</p>

---

### Validation Summary

| Metric | Value |
|---------|-------|
| EEG Dataset | BCI Competition IV Dataset 2b |
| Subjects | 9 |
| Recordings Analysed | 45 |
| EEG Channel | C3 |
| Band-pass Filter | 1–45 Hz |
| Alpha Peak Search Window | 8–13 Hz |
| Kuramoto Oscillators | 50 |
| Coupling Strength | K = 2.0 |
| Mean Natural Frequency | 10.0 Hz |
| Frequency Standard Deviation | 0.3 Hz |
| Synthetic Alpha Peak | **10.254 Hz** |
| Average EEG Alpha Peak | **10.664 Hz** |
| Mean Absolute Peak Difference | **0.692 Hz** |

The Kuramoto oscillator network reproduced the dominant alpha-band frequency across all analysed EEG recordings with an average peak difference of less than **0.7 Hz**.

---

## Example Output

The project automatically generates:

- Individual spectrum comparisons for each EEG recording
- Average EEG power spectrum
- Final comparison between the synthetic Kuramoto spectrum and the averaged EEG spectrum
- Summary statistics (`summary.csv`)
- Technical report describing methodology and results

Example outputs are available in the `output/` directory.

---

## Project Structure

```text
kuramoto-eeg/
│
├── data/
│   └── bci_iv/
│
├── src/
│   ├── kuramoto.py
│   ├── spectrum.py
│   └── run.py
│
├── output/
│   ├── linear scale plots/
│   ├── log scale plots/
│   ├── summary.csv
│   └── writeup.md
│
├── requirements.txt
└── README.md
```

---

## Methodology

### Synthetic EEG

The synthetic signal is generated using a network of **50 all-to-all coupled Kuramoto oscillators**.

Natural frequencies are sampled from

- Mean = **10 Hz**
- Standard deviation = **0.3 Hz**

The system is integrated using SciPy's **RK45** solver, and the synthetic EEG proxy is obtained by averaging the sine of all oscillator phases.

---

### Real EEG

EEG recordings are obtained from the **BCI Competition IV Dataset 2b**.

For each recording:

- Channel **C3** is extracted.
- A **1–45 Hz** band-pass filter is applied.
- Welch's method is used to estimate the power spectral density.
- The dominant alpha-band peak is identified between **8–13 Hz**.

---

### Spectral Comparison

For every EEG recording:

1. Compute the synthetic PSD.
2. Compute the real EEG PSD.
3. Identify the dominant alpha-band peak.
4. Calculate the frequency difference.
5. Generate an overlay comparison plot.

Finally, all EEG spectra are averaged to produce a representative spectrum for comparison with the Kuramoto model.

---

## Technologies / Libraries Used

- Python
- NumPy
- SciPy
- MNE-Python
- Matplotlib
- Pandas

---

## Running the Project

Install dependencies

```bash
pip install -r requirements.txt
```

Run the analysis

```bash
python src/run.py
```

Outputs will be generated automatically inside the `output/` directory.

---

## Technical Report

A detailed explanation of the model, parameter selection, validation methodology, and complete experimental results is available in:

```text
output/writeup.md
```

---

## Future Improvements

- Subject-specific parameter optimization
- Multi-population Kuramoto networks
- Structural connectivity constraints
- Time-varying coupling strengths
- Stochastic oscillator dynamics
- Functional connectivity analysis
- Comparison with additional open EEG datasets

---

## Motivation

This project was completed as the first milestone in a computational neuroscience learning roadmap.

The primary objective was to build a complete end-to-end neuroscience project within three days while learning the fundamentals of dynamical systems, synchronization, EEG spectral analysis, and computational modeling.

Rather than maximizing model complexity, the emphasis was on developing a reproducible workflow that combines mathematical modeling with experimental EEG validation.

---

## References

- Kuramoto, Y. *Chemical Oscillations, Waves, and Turbulence*. Springer, 1984.
- BCI Competition IV Dataset 2b.
- MNE-Python Documentation.
- SciPy Signal Processing Documentation.

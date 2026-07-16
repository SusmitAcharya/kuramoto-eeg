import os
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from kuramoto import run_kuramoto
from spectrum import (
    load_real_eeg,
    compute_real_spectrum,
    compute_synthetic_spectrum,
)


# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------

def normalize_psd(psd):
    """Normalize a PSD to unit peak power."""
    return psd / np.max(psd)


def find_peak_freq(freqs, psd, fmin=1.0, fmax=45.0):
    """Return dominant frequency within a specified frequency band."""
    mask = (freqs >= fmin) & (freqs <= fmax)
    idx = np.argmax(psd[mask])
    return freqs[mask][idx]


# ------------------------------------------------------------
# Global Plot Theme (GitHub Dark)
# ------------------------------------------------------------
plt.rcParams.update({
    "figure.facecolor": "#0d1117",
    "axes.facecolor": "#161b22",
    "savefig.facecolor": "#0d1117",
    "axes.edgecolor": "#30363d",
    "axes.labelcolor": "#f0f6fc",
    "axes.titlecolor": "#f0f6fc",
    "xtick.color": "#8b949e",
    "ytick.color": "#8b949e",
    "text.color": "#f0f6fc",
    "grid.color": "#30363d",
    "grid.alpha": 0.45,
    "legend.facecolor": "#161b22",
    "legend.edgecolor": "#30363d",
    "font.size": 12,
})
EEG_COLOR = "#58a6ff"
KURAMOTO_COLOR = "#ff7b72"
ALPHA_COLOR = "#2f81f7"


def style_axes(ax):
    ax.grid(True, which="major", linestyle="--", linewidth=0.6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#30363d")
    ax.spines["bottom"].set_color("#30363d")
    ax.axvspan(8, 13, color=ALPHA_COLOR, alpha=0.08, zorder=0)


def glow_line(ax, x, y, color, label=None, lw=2.8):
    ax.plot(x, y, color=color, linewidth=8, alpha=0.12, solid_capstyle="round")
    return ax.plot(x, y, color=color, linewidth=lw, label=label, solid_capstyle="round")[0]


def make_comparison_plot(freqs_synth, psd_synth_norm, freqs_real, psd_real_norm,
                          peak_synth, peak_real, title, save_path, log_scale=False):
    """
    Build one Kuramoto-vs-EEG comparison plot, either linear or log y-axis.
    """
    plt.figure(figsize=(12, 6))
    ax = plt.gca()

    if log_scale:
        ax.set_yscale("log")

    glow_line(ax, freqs_synth, psd_synth_norm, KURAMOTO_COLOR, label="Kuramoto")
    glow_line(ax, freqs_real, psd_real_norm, EEG_COLOR, label=title.split("\n")[0])

    plt.axvline(peak_synth, linestyle="--")
    plt.axvline(peak_real, linestyle="--")

    plt.xlim(0, 45)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Normalized PSD")
    plt.title(title)
    plt.legend()

    style_axes(ax)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200)
    plt.close()


# ------------------------------------------------------------
# Output directories
# ------------------------------------------------------------

linear_dir = Path("output/linear scale plots")
log_dir = Path("output/log scale plots")
linear_dir.mkdir(parents=True, exist_ok=True)
log_dir.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# Synthetic EEG (Kuramoto)
# ------------------------------------------------------------

dt = 0.001
fs = 1 / dt

K = 2.0
freq_mean_hz = 10.0
freq_std_hz = 0.3

t, signal, theta = run_kuramoto(
    K=K,
    freq_mean_hz=freq_mean_hz,
    freq_std_hz=freq_std_hz,
)

freqs_synth, psd_synth = compute_synthetic_spectrum(signal, fs)

peak_synth = find_peak_freq(freqs_synth, psd_synth, fmin=5, fmax=15)

psd_synth_norm = normalize_psd(psd_synth)


# ------------------------------------------------------------
# Load EEG Files
# ------------------------------------------------------------

data_dir = Path("data/bci_iv")
files = sorted(data_dir.glob("*.gdf"))

if len(files) == 0:
    raise FileNotFoundError("No GDF files found in data/bci_iv")

all_psds = []
summary = []
freqs_real = None

print(f"Found {len(files)} EEG recordings.\n")


# ------------------------------------------------------------
# Individual Comparisons (linear + log)
# ------------------------------------------------------------

for file in files:

    print(f"Processing {file.name}")

    raw = load_real_eeg(str(file), channel="C3")
    freqs, psd = compute_real_spectrum(raw)

    if freqs_real is None:
        freqs_real = freqs
    else:
        if not np.allclose(freqs_real, freqs):
            raise ValueError(f"Frequency axis mismatch in {file.name}")

    all_psds.append(psd)

    peak_real = find_peak_freq(freqs, psd, fmin=8, fmax=13)

    summary.append([file.stem, peak_real, peak_synth, abs(peak_real - peak_synth)])

    psd_norm = normalize_psd(psd)
    title = (
        f"{file.stem}\n"
        f"Kuramoto Peak = {peak_synth:.2f} Hz | "
        f"EEG Peak = {peak_real:.2f} Hz"
    )

    make_comparison_plot(
        freqs_synth, psd_synth_norm, freqs, psd_norm,
        peak_synth, peak_real, title,
        linear_dir / f"comparison_{file.stem}.png",
        log_scale=False,
    )

    make_comparison_plot(
        freqs_synth, psd_synth_norm, freqs, psd_norm,
        peak_synth, peak_real, title,
        log_dir / f"comparison_{file.stem}.png",
        log_scale=True,
    )

print("\nFinished individual comparisons.\n")


# ------------------------------------------------------------
# Average EEG Spectrum
# ------------------------------------------------------------

all_psds = np.vstack(all_psds)
mean_psd = np.mean(all_psds, axis=0)
std_psd = np.std(all_psds, axis=0)

mean_norm = normalize_psd(mean_psd)
lower = normalize_psd(np.maximum(mean_psd - std_psd, 1e-12))
upper = normalize_psd(mean_psd + std_psd)

peak_avg = find_peak_freq(freqs_real, mean_psd, fmin=5, fmax=15)


def make_average_plot(save_path, log_scale=False):
    plt.figure(figsize=(12, 6))
    ax = plt.gca()

    if log_scale:
        ax.set_yscale("log")

    glow_line(ax, freqs_real, mean_norm, EEG_COLOR, label="Average EEG")
    ax.fill_between(freqs_real, lower, upper, alpha=0.30, label="±1 SD")

    plt.axvline(peak_avg, linestyle="--")
    plt.xlim(0, 45)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Normalized PSD")
    plt.title("Average EEG Spectrum")
    plt.legend()

    style_axes(ax)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200)
    plt.close()


make_average_plot(linear_dir / "average_eeg.png", log_scale=False)
make_average_plot(log_dir / "average_eeg.png", log_scale=True)


# ------------------------------------------------------------
# Final Comparison
# ------------------------------------------------------------

def make_final_comparison_plot(save_path, log_scale=False):
    plt.figure(figsize=(12, 6))
    ax = plt.gca()

    if log_scale:
        ax.set_yscale("log")

    ax.plot(freqs_synth, psd_synth_norm, linewidth=2, label="Kuramoto", color=KURAMOTO_COLOR)
    glow_line(ax, freqs_real, mean_norm, EEG_COLOR, label="Average EEG")
    ax.fill_between(freqs_real, lower, upper, alpha=0.25)

    plt.axvline(peak_synth, linestyle="--")
    plt.axvline(peak_avg, linestyle="--")

    plt.xlim(0, 45)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Normalized PSD")
    plt.title("Kuramoto vs Average EEG")
    plt.legend()

    style_axes(ax)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200)
    plt.close()


make_final_comparison_plot(linear_dir / "final_average_comparison.png", log_scale=False)
make_final_comparison_plot(log_dir / "final_average_comparison.png", log_scale=True)


# ------------------------------------------------------------
# Save Summary
# ------------------------------------------------------------

summary_df = pd.DataFrame(
    summary,
    columns=["Subject", "EEG Peak (Hz)", "Kuramoto Peak (Hz)", "Difference (Hz)"],
)

summary_df.loc[len(summary_df)] = [
    "Average",
    summary_df["EEG Peak (Hz)"].mean(),
    peak_synth,
    summary_df["Difference (Hz)"].mean(),
]

summary_df.to_csv("output/summary.csv", index=False)

print(summary_df)

print("\n---------------- Summary Statistics ----------------")
print(f"Mean EEG peak      : {summary_df.iloc[:-1]['EEG Peak (Hz)'].mean():.2f} Hz")
print(f"Std EEG peak       : {summary_df.iloc[:-1]['EEG Peak (Hz)'].std():.2f} Hz")
print(f"Mean peak error    : {summary_df.iloc[:-1]['Difference (Hz)'].mean():.2f} Hz")
print(f"Maximum peak error : {summary_df.iloc[:-1]['Difference (Hz)'].max():.2f} Hz")
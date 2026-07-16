import matplotlib.pyplot as plt
plt.rcParams.update({'figure.facecolor':'#0d1117','axes.facecolor':'#161b22','savefig.facecolor':'#0d1117','text.color':'#f0f6fc','axes.labelcolor':'#f0f6fc','axes.titlecolor':'#f0f6fc','xtick.color':'#8b949e','ytick.color':'#8b949e'})
import numpy as np
import mne
from scipy.signal import welch

from kuramoto import run_kuramoto


# ------------------------------------------------------------
# Synthetic EEG
# ------------------------------------------------------------

def compute_synthetic_spectrum(
    signal,
    fs,
    nperseg=2048,
):
    """
    Compute the power spectral density (PSD) of the synthetic Kuramoto
    signal using Welch's method.

    Parameters
    ----------
    signal : ndarray
        Synthetic EEG signal.
    fs : float
        Sampling frequency (Hz).
    nperseg : int
        Segment length for Welch PSD.

    Returns
    -------
    freqs : ndarray
        Frequency axis.
    psd : ndarray
        Power spectral density.
    """

    freqs, psd = welch(
        signal,
        fs=fs,
        nperseg=nperseg,
        detrend="constant",
    )

    return freqs, psd


# ------------------------------------------------------------
# Real EEG
# ------------------------------------------------------------

def load_real_eeg(
    gdf_path,
    channel="C3",
    l_freq=1.0,
    h_freq=45.0,
):
    """
    Load a BCI Competition IV Dataset 2b GDF recording.

    Steps
    -----
    1. Read GDF file
    2. Select one EEG channel
    3. Apply 1-45 Hz bandpass filter

    Returns
    -------
    raw : mne.io.Raw
        Preprocessed MNE Raw object.
    """

    raw = mne.io.read_raw_gdf(
        gdf_path,
        preload=True,
        verbose=False,
    )

    raw.pick(f"EEG:{channel}")

    print(
        f"Loaded {gdf_path} | Channel={channel}"
    )

    raw.filter(
        l_freq=l_freq,
        h_freq=h_freq,
        verbose=False,
    )

    return raw


def compute_real_spectrum(
    raw,
    fmin=1.0,
    fmax=45.0,
    n_fft=2048,
    n_per_seg=2048,
):
    """
    Compute Welch PSD from an MNE Raw object.

    Returns
    -------
    freqs : ndarray
        Frequency axis.
    power : ndarray
        Power spectral density.
    """

    psd = raw.compute_psd(
        method="welch",
        fmin=fmin,
        fmax=fmax,
        n_fft=n_fft,
        n_per_seg=n_per_seg,
        verbose=False,
    )

    freqs = psd.freqs
    power = psd.get_data().squeeze()

    return freqs, power


# ------------------------------------------------------------
# Standalone Test
# ------------------------------------------------------------

if __name__ == "__main__":

    # -----------------------------
    # Synthetic EEG
    # -----------------------------

    dt = 0.001
    fs = 1 / dt

    t, signal, theta = run_kuramoto(
        K=2.0,
        freq_std_hz=0.3,
    )

    freqs_synth, psd_synth = compute_synthetic_spectrum(
        signal,
        fs,
    )

    # -----------------------------
    # Real EEG
    # -----------------------------

    gdf_path = "data/bci_iv/B0101T.gdf"

    raw = load_real_eeg(
        gdf_path,
        channel="C3",
    )

    freqs_real, psd_real = compute_real_spectrum(raw)

    # -----------------------------
    # First 5-minute check
    # -----------------------------

    duration = min(
        300,
        raw.times[-1],
    )

    raw_short = raw.copy().crop(
        tmin=0,
        tmax=duration,
    )

    freqs_short, psd_short = compute_real_spectrum(
        raw_short,
    )

    # -----------------------------
    # Plot
    # -----------------------------

    fig, axes = plt.subplots(
        1,
        3,
        figsize=(18, 5),
    )

    axes[0].semilogy(
        freqs_synth,
        psd_synth,
    )

    axes[0].set_xlim(0, 45)
    axes[0].set_title("Synthetic PSD")
    axes[0].set_xlabel("Frequency (Hz)")
    axes[0].set_ylabel("Power")

    axes[1].semilogy(
        freqs_real,
        psd_real,
    )

    axes[1].set_xlim(0, 45)
    axes[1].set_title("Real EEG PSD")
    axes[1].set_xlabel("Frequency (Hz)")

    axes[2].semilogy(
        freqs_short,
        psd_short,
    )

    axes[2].set_xlim(0, 45)
    axes[2].set_title("First 5 Minutes PSD")
    axes[2].set_xlabel("Frequency (Hz)")

    plt.tight_layout()
    plt.show()

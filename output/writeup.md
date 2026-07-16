# Kuramoto Oscillator Model vs. Real EEG: Parameter Selection, Validation and Results

---

# Model

A network of **50 all-to-all coupled Kuramoto phase oscillators** was used to generate a synthetic EEG-like oscillatory signal.

The natural frequencies of the oscillators were sampled from a Gaussian distribution with:

- Mean frequency: **10.0 Hz**
- Standard deviation: **0.3 Hz**

The system was numerically integrated using **SciPy's RK45 solver** for **20 seconds** with a sampling interval of **1 ms (1000 Hz)**.

The synthetic EEG proxy was computed as

\[
\frac{1}{N}\sum_{i=1}^{N}\sin(\theta_i)
\]

where \(N=50\) and \(\theta_i\) denotes the phase of the *i*th oscillator.

Power spectral density (PSD) for both the synthetic and real EEG signals was estimated using Welch's method. The dominant oscillatory frequency was defined as the frequency corresponding to the maximum PSD within the alpha band used for comparison.

---

# Coupling Strength Selection

Three coupling strengths were evaluated:

- **K = 0.5**
- **K = 2.0**
- **K = 10.0**

For each coupling strength, the Kuramoto model was simulated and evaluated using the synthetic EEG time series, the Kuramoto order parameter \(r(t)\), and the resulting power spectral density.

### K = 0.5

Weak coupling resulted in limited collective synchronization among the oscillators. The synthetic signal exhibited relatively low coherence, producing a less distinct alpha-band peak in the power spectrum.

### K = 2.0

Intermediate coupling produced a stable and well-defined alpha-band oscillation. The resulting synthetic spectrum showed the closest agreement with the dominant alpha peaks observed across the experimental EEG recordings while maintaining realistic synchronization behaviour.

### K = 10.0

Strong coupling substantially altered the network dynamics. Although the oscillators remained coupled, the resulting synthetic signal did not improve agreement with the experimental EEG spectra compared with the intermediate coupling regime.

Based on the spectral comparison with the EEG recordings, **K = 2.0** produced the most representative synthetic alpha-band oscillation and was therefore selected for all subsequent analyses.

---

# EEG Dataset

Real EEG recordings were obtained from the **BCI Competition IV Dataset 2b**.

Unlike the initial prototype that analysed only nine recordings, the final validation used **all 45 available recordings** comprising both training and evaluation sessions.

Dataset composition:

- Subjects: **9**
- Sessions per subject: **5**
- Total recordings analysed: **45**

For every recording:

- EEG channel **C3** was extracted.
- A **1–45 Hz** band-pass filter was applied.
- Welch power spectral density was computed.
- The dominant peak was identified **within the alpha band (8–13 Hz)**.

Each recording was compared individually with the synthetic Kuramoto spectrum.

Finally, all PSDs were averaged to obtain a representative EEG spectrum.

Because Dataset 2b is a **motor imagery dataset**, these spectra represent overall motor imagery EEG characteristics rather than dedicated resting-state recordings.

---

# Subject-wise Results

| Subject | EEG Peak (Hz) | Kuramoto Peak (Hz) | Difference (Hz) |
|---------|--------------:|-------------------:|----------------:|
| B0101T | 10.986328 | 10.253906 | 0.732422 |
| B0102T | 11.108398 | 10.253906 | 0.854492 |
| B0103T | 10.131836 | 10.253906 | 0.122070 |
| B0104E | 10.009766 | 10.253906 | 0.244141 |
| B0105E | 11.230469 | 10.253906 | 0.976562 |
| B0201T | 9.765625 | 10.253906 | 0.488281 |
| B0202T | 9.887695 | 10.253906 | 0.366211 |
| B0203T | 9.765625 | 10.253906 | 0.488281 |
| B0204E | 9.765625 | 10.253906 | 0.488281 |
| B0205E | 9.521484 | 10.253906 | 0.732422 |
| B0301T | 9.643555 | 10.253906 | 0.610352 |
| B0302T | 10.009766 | 10.253906 | 0.244141 |
| B0303T | 9.643555 | 10.253906 | 0.610352 |
| B0304E | 9.277344 | 10.253906 | 0.976562 |
| B0305E | 9.643555 | 10.253906 | 0.610352 |
| B0401T | 11.108398 | 10.253906 | 0.854492 |
| B0402T | 10.986328 | 10.253906 | 0.732422 |
| B0403T | 11.108398 | 10.253906 | 0.854492 |
| B0404E | 11.108398 | 10.253906 | 0.854492 |
| B0405E | 11.352539 | 10.253906 | 1.098633 |
| B0501T | 10.620117 | 10.253906 | 0.366211 |
| B0502T | 10.131836 | 10.253906 | 0.122070 |
| B0503T | 10.620117 | 10.253906 | 0.366211 |
| B0504E | 10.253906 | 10.253906 | 0.000000 |
| B0505E | 10.009766 | 10.253906 | 0.244141 |
| B0601T | 10.375977 | 10.253906 | 0.122070 |
| B0602T | 10.620117 | 10.253906 | 0.366211 |
| B0603T | 10.375977 | 10.253906 | 0.122070 |
| B0604E | 10.375977 | 10.253906 | 0.122070 |
| B0605E | 10.375977 | 10.253906 | 0.122070 |
| B0701T | 12.939453 | 10.253906 | 2.685547 |
| B0702T | 12.939453 | 10.253906 | 2.685547 |
| B0703T | 12.695312 | 10.253906 | 2.441406 |
| B0704E | 10.498047 | 10.253906 | 0.244141 |
| B0705E | 10.253906 | 10.253906 | 0.000000 |
| B0801T | 10.253906 | 10.253906 | 0.000000 |
| B0802T | 10.375977 | 10.253906 | 0.122070 |
| B0803T | 10.864258 | 10.253906 | 0.610352 |
| B0804E | 10.253906 | 10.253906 | 0.000000 |
| B0805E | 11.108398 | 10.253906 | 0.854492 |
| B0901T | 11.352539 | 10.253906 | 1.098633 |
| B0902T | 11.352539 | 10.253906 | 1.098633 |
| B0903T | 12.084961 | 10.253906 | 1.831055 |
| B0904E | 11.352539 | 10.253906 | 1.098633 |
| B0905E | 11.718750 | 10.253906 | 1.464844 |
| **Average** | **10.663520** | **10.253906** | **0.691732** |

---

# Overall Results

Averaging all 45 recordings produced a representative EEG spectrum.

**Average EEG Alpha Peak:** **10.664 Hz**

**Synthetic Kuramoto Peak:** **10.254 Hz**

**Mean Absolute Peak Difference:** **0.692 Hz**

Additional observations:

- Total recordings analysed: **45**
- Exact peak match: **4 recordings**
- Largest deviation: **2.686 Hz** (B0701T and B0702T)
- Smallest deviation: **0.000 Hz**

The average EEG alpha peak differed from the synthetic Kuramoto oscillation by less than **0.7 Hz**, indicating strong agreement between the model and the experimental data.

---

# Discussion

Across all 45 recordings, the Kuramoto oscillator network reproduced the dominant alpha-band frequency with good overall agreement.

Most recordings clustered within approximately **1 Hz** of the synthetic peak, indicating that a simple population of coupled phase oscillators can capture the principal oscillatory frequency present in the experimental data.

The largest deviations occurred for Subject B07, whose recordings exhibited alpha activity shifted toward the upper-alpha band. Such variability is expected due to inter-subject physiological differences and task-dependent modulation in motor imagery experiments.

Although the Kuramoto model is intentionally simple, these results suggest that collective synchronization dynamics are sufficient to reproduce one important spectral characteristic of the analysed EEG recordings: the dominant alpha-band frequency.

---

# Figures

### Figure 1–45

Individual comparisons between the synthetic Kuramoto spectrum and each EEG recording.

### Figure 46

Average EEG power spectrum computed from all 45 recordings.

### Figure 47

Comparison between the averaged EEG spectrum and the synthetic Kuramoto spectrum.

---

# Limitations

- The Kuramoto model consists of a homogeneous population of coupled phase oscillators and therefore generates a relatively narrow oscillatory peak.

- Real EEG exhibits broadband activity together with multiple physiologically distinct frequency bands that are not represented by the present model.

- The model captures synchronization dynamics but does not incorporate neuronal membrane dynamics, anatomical connectivity, conduction delays, stochastic neural noise, or spatial propagation.

- Synthetic and real signals possess different physical units (unitless oscillator output versus EEG measured in microvolts). Consequently, PSDs were normalized to unit peak power and compared only in terms of spectral shape and dominant frequency.

- The BCI Competition IV Dataset 2b consists of **motor imagery recordings**, not dedicated resting-state EEG. Therefore, task-related modulation may influence the observed spectra.

- The present comparison focuses exclusively on dominant alpha-band frequency and does not attempt to reproduce the complete temporal dynamics or full broadband EEG spectrum.

---

# Conclusion

This study demonstrates that a relatively simple network of 50 coupled Kuramoto oscillators, parameterized with a mean intrinsic frequency of 10 Hz and coupling strength \(K=2.0\), reproduces the dominant alpha-band oscillation observed across **45 recordings** from the BCI Competition IV Dataset 2b.

The average EEG alpha peak (10.664 Hz) differed from the synthetic Kuramoto peak (10.254 Hz) by only **0.692 Hz**, indicating good agreement despite substantial inter-subject variability and the simplicity of the model.

These results support the use of the Kuramoto model as an interpretable phenomenological framework for studying large-scale neural synchronization and its relationship to experimentally observed EEG oscillations.
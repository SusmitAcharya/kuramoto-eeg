import matplotlib.pyplot as plt
plt.rcParams.update({'figure.facecolor':'#0d1117','axes.facecolor':'#161b22','savefig.facecolor':'#0d1117','text.color':'#f0f6fc','axes.labelcolor':'#f0f6fc','axes.titlecolor':'#f0f6fc','xtick.color':'#8b949e','ytick.color':'#8b949e'})
import numpy as np
from scipy.integrate import solve_ivp


def kuramoto_deriv(t, theta, omega, K, N):
    """
    Compute the time derivative of the Kuramoto phase oscillators.

    Parameters
    ----------
    t : float
        Current time (unused, required by solve_ivp).
    theta : ndarray
        Current oscillator phases, shape (N,).
    omega : ndarray
        Natural angular frequencies (rad/s).
    K : float
        Coupling strength.
    N : int
        Number of oscillators.

    Returns
    -------
    ndarray
        Phase derivatives d(theta)/dt.
    """
    diffs = theta[:, None] - theta[None, :]
    coupling = (K / N) * np.sum(np.sin(-diffs), axis=1)
    return omega + coupling


def run_kuramoto(
    N=50,
    K=10.0,
    freq_mean_hz=10.0,
    freq_std_hz=1.5,
    duration=20.0,
    dt=0.001,
    seed=42,
):
    """
    Simulate an all-to-all coupled Kuramoto oscillator network.

    Parameters
    ----------
    N : int
        Number of oscillators.
    K : float
        Coupling strength.
    freq_mean_hz : float
        Mean natural frequency (Hz).
    freq_std_hz : float
        Standard deviation of natural frequencies (Hz).
    duration : float
        Simulation duration (s).
    dt : float
        Sampling interval (s).
    seed : int
        Random seed.

    Returns
    -------
    t : ndarray
        Time vector.
    signal : ndarray
        Mean synthetic EEG proxy.
    theta : ndarray
        Oscillator phases (N × T).
    """

    rng = np.random.default_rng(seed)

    # Convert natural frequencies from Hz to rad/s
    omega = 2 * np.pi * rng.normal(
        freq_mean_hz,
        freq_std_hz,
        N,
    )

    # Random initial phases
    theta0 = rng.uniform(
        0,
        2 * np.pi,
        N,
    )

    t_eval = np.linspace(
        0,
        duration,
        int(duration / dt) + 1,
    )

    sol = solve_ivp(
        kuramoto_deriv,
        (0, duration),
        theta0,
        args=(omega, K, N),
        method="RK45",
        t_eval=t_eval,
        dense_output=False,
    )

    if not sol.success:
        raise RuntimeError(
            f"Kuramoto integration failed: {sol.message}"
        )

    # Mean oscillator output used as a synthetic EEG proxy
    signal = np.mean(
        np.sin(sol.y),
        axis=0,
    )

    return sol.t, signal, sol.y


def order_parameter(theta):
    """
    Compute the Kuramoto order parameter.

    Parameters
    ----------
    theta : ndarray
        Oscillator phases with shape (N, T).

    Returns
    -------
    ndarray
        Synchronization order parameter r(t), ranging from
        0 (fully desynchronized) to 1 (fully synchronized).
    """
    return np.abs(
        np.mean(
            np.exp(1j * theta),
            axis=0,
        )
    )


if __name__ == "__main__":

    K_values = [0.5, 2.0, 10.0]
    freq_std_hz = 0.3

    fig, axes = plt.subplots(
        3,
        2,
        figsize=(12, 8),
        sharex=True,
    )

    for row, K in enumerate(K_values):

        t, signal, theta = run_kuramoto(
            K=K,
            freq_std_hz=freq_std_hz,
        )

        r = order_parameter(theta)

        print(
            f"K = {K:>4} | "
            f"Samples = {len(signal)} | "
            f"Final r = {r[-1]:.3f}"
        )

        # Synthetic signal
        axes[row,0].plot(t, signal, linewidth=7, alpha=0.12, color='#58a6ff')
        axes[row,0].plot(t, signal, linewidth=2.6, color='#58a6ff')
        axes[row, 0].set_title(f"Synthetic Signal (K={K})")
        axes[row, 0].set_ylabel("Mean sin(θ)")

        # Order parameter
        axes[row,1].plot(t, r, linewidth=7, alpha=0.10, color='#ff7b72')
        axes[row,1].plot(t, r, linewidth=2.6, color='#ff7b72')
        axes[row, 1].set_title(f"Order Parameter r(t) (K={K})")
        axes[row, 1].set_ylabel("r")
        axes[row, 1].set_ylim(0, 1.05)

    axes[-1, 0].set_xlabel("Time (s)")
    axes[-1, 1].set_xlabel("Time (s)")

    plt.tight_layout()
    plt.show()

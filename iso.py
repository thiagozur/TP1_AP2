import numpy as np
from funciones import calc_eta_total, calc_radfree, calc_radforced

def iso(f, m, eta, dim, fc, rho0 = 1.18, c0 = 343):
    array = np.zeros_like(f, dtype=float)

    l1 = max(dim[0], dim[1])
    l2 = min(dim[0], dim[1])

    for i, f in enumerate(f):
        eta_total = calc_eta_total(f, m, eta)
        sig = calc_radfree(f, fc, dim, c0)
        sigf = calc_radforced(f, dim, c0)

        if f > fc:
            tau = (((2 * rho0 * c0) / (2 * np.pi * f * m)) ** 2) * ((np.pi * fc * (sig ** 2)) / (2 * f * eta_total))
        elif f < fc:
            tau = (((2 * rho0 * c0) / (2 * np.pi * f * m)) ** 2) * (2 * sigf + (((l1 + l2) ** 2) / (l1 ** 2 + l2 ** 2)) * np.sqrt(fc / f) * ((sig ** 2) / eta_total))
        else:
            tau = (((2 * rho0 * c0) / (2 * np.pi * f * m)) ** 2) * ((np.pi * (sig ** 2)) / (2 * eta_total))
        
        array[i] = -10 * np.log10(tau)

    return array
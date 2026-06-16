import numpy as np
from funciones import calc_eta_total, calc_radfree, calc_radforced

def iso(f, material, fc, rho0 = 1.18, c0 = 343):
    array = np.zeros_like(f, dtype=float)

    l1 = max(material.dim[0], material.dim[1])
    l2 = min(material.dim[0], material.dim[1])

    for i, f in enumerate(f):
        eta_total = calc_eta_total(f, material)
        sig = calc_radfree(f, fc, material, c0)
        sigf = calc_radforced(f, material, c0)

        if f > fc:
            tau = (((2 * rho0 * c0) / (2 * np.pi * f * material.m)) ** 2) * ((np.pi * fc * (sig ** 2)) / (2 * f * eta_total))
        elif f < fc:
            tau = (((2 * rho0 * c0) / (2 * np.pi * f * material.m)) ** 2) * (2 * sigf + (((l1 + l2) ** 2) / (l1 ** 2 + l2 ** 2)) * np.sqrt(fc / f) * ((sig ** 2) / eta_total))
        else:
            tau = (((2 * rho0 * c0) / (2 * np.pi * f * material.m)) ** 2) * ((np.pi * (sig ** 2)) / (2 * eta_total))
        
        array[i] = -10 * np.log10(tau)

    return array
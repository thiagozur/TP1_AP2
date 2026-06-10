import numpy as np
from funciones import calc_eta_total

def sharp1(f, m, rho0 = 1.18, c0 = 343):
    r = 10 * np.log10(1 + ((np.pi * m * f) / (rho0 * c0)) ** 2) - 5.5
    return r

def sharp3(f, m, eta, fc, rho0 = 1.18, c0 = 343):
    r1 = 10 * np.log10(1 + ((np.pi * m * f) / (rho0 * c0)) ** 2) + 10 * np.log10((2 * calc_eta_total(f, m, eta) * f) / (np.pi * fc))
    r2 = 10 * np.log10(1 + ((np.pi * m * f) / (rho0 * c0)) ** 2) - 5.5
    r = np.minimum(r1, r2)
    return r

def sharp(f, m, eta, fc, rho0 = 1.18, c0 = 343):
    array = np.zeros_like(f, dtype=float)
    
    for i, f in enumerate(f):
        if f < (0.5 * fc):
            array[i] = sharp1(f, m, rho0, c0)
        elif (0.5 * fc) <= f and f < fc:
            sharp1_end = sharp1(0.5 * fc, m, rho0, c0)
            sharp3_start = sharp3(fc, m, eta, fc, rho0, c0)
            array[i] = np.interp(f, [0.5 * fc, fc], [sharp1_end, sharp3_start])
        else:
            array[i] = sharp3(f, m, eta, fc, rho0)

    return array
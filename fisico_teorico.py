import numpy as np
from funciones import ley_masa

def ley_masa_corr(f, m, eta, fc, rho0 = 1.18, c0 = 343):
    w = 2 * np.pi * f
    wc = 2 * np.pi * fc
    r = 20 * np.log10((w * m) / (2 * rho0 * c0)) - 10 * np.log10(np.pi / (4 * eta)) + 10 * np.log10(w / wc) + 10 * np.log10(1 - (wc / w)) - 5
    return r

def fisico_teorico(f, m, eta, fc, fd, rho0 = 1.18, c0 = 343):
    array = np.zeros_like(f, dtype=float)
    
    for i, f in enumerate(f):
        if f > fc and f <= fd:
            array[i] = ley_masa_corr(f, m, eta, fc, rho0 = 1.18, c0 = 343)
        else:
            array[i] = ley_masa(f, m)

    return array
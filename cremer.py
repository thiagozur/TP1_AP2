import numpy as np
from funciones import calc_eta_total, ley_masa

def cremer(f, material, fc, fd):
    array = np.zeros_like(f, dtype=float)

    for i, f in enumerate(f):  
        if f > fc and f <= fd:
            array[i] = 20 * np.log10(material.m * f) - 10 * np.log10(np.pi / (4 * calc_eta_total(f, material))) + 10 * np.log10(f / fc) - 10 * np.log10(fc / (f - fc)) - 47
        else:
            array[i] = ley_masa(f, material)

    return array
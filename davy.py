import numpy as np
from funciones import calc_eta_total, sigma as sig, shear

def davy_panel_simple(f, material, fc, rho0 = 1.18, c0 = 343):
    cos21max = 0.9

    rho_sup = material.rho * material.dim[2]

    normal = rho0 * c0 / (np.pi * f * rho_sup)
    normal2 = normal ** 2

    esp = 2 * material.dim[0] * material.dim[1] / (material.dim[0] + material.dim[1])

    cos2l = c0 / (2 * np.pi * f * esp)

    if cos2l > cos21max:
        cos2l = cos21max

    tau1 = normal2 * np.log((normal2 + 1) / (normal2 + cos2l))

    ratio = f / fc

    r = 1 - 1 / ratio

    if r < 0:
        r = 0
    
    g = np.sqrt(r)

    rad = sig(g, f, material, c0)
    rad2 = rad ** 2

    netatotal = calc_eta_total(f, material) + rad * normal

    z = 2 / netatotal

    y = np.arctan(z) - np.arctan(z * (1 - ratio))

    tau2 = normal2 * rad2 * y / (netatotal * 2 * ratio)
    tau2 *= shear(f, material.rho, material.e, material.sigma, material.dim)

    if f < fc:
        tau = tau1 + tau2
    else:
        tau = tau2
    
    panel_simple = -10 * np.log10(tau)

    return panel_simple

def davy(f, material, fc, rho0 = 1.18, c0 = 343):
    array = np.zeros_like(f, dtype=float)

    limit = 2 ** (1 / (2 * 3))
    averages = 3

    for i, f in enumerate(f):
        ratio = f / fc

        if ratio < (1 / limit) or ratio > limit:
            array[i] = davy_panel_simple(f, material, fc, rho0, c0)
        else:
            av_panel_simple = 0.0

            for j in range(1, averages + 1):
                factor = 2 ** ((2 * j - 1 - averages) / (2 * averages * 3))
                f_aux = f * factor

                r_aux = davy_panel_simple(f_aux, material, fc, rho0, c0)

                aux = 10 ** (-r_aux / 10)
                av_panel_simple += aux
            
            array[i] = -10 * np.log10(av_panel_simple / averages)

    return array
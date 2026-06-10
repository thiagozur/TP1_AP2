import numpy as np

def calc_m(rho, dim):
    m = rho * dim[2]
    return m

def calc_b(e, sigma, dim):
    b = (e * (dim[2] ** 3)) / (12 * (1 - sigma ** 2))
    return b

def calc_fc(e, rho, dim, c0 = 343):
    fc = ((c0 ** 2) / (1.8 * dim[2])) * np.sqrt(rho / e)
    return fc

def calc_fd(m, e, b, rho):
    fd = (e / (2 * np.pi * rho)) * np.sqrt(m / b)
    return fd

def calc_f11(fc, dim, c0):
    f11 = ((c0 ** 2) / (4 * fc)) * ((1 / dim[0]) + (1 / dim[1]))
    return f11

def calc_eta_total(f, m, eta):
    eta_total = eta + (m / (485 * np.sqrt(f)))
    return eta_total

def ley_masa(f, m):
    r = 20 * np.log10(m * f) - 47
    return r

def sigma(g, f, dim, c0 = 343):
    w = 1.3
    beta = 0.234
    n = 2

    s = dim[0] * dim[1]
    u = 2 * (dim[0] + dim[1])

    twoa = 4 * (s / u)

    k = 2 * np.pi * f / c0
    f_lim = w * np.sqrt(np.pi / (k * twoa))

    if f_lim > 1:
        f_lim = 1
    
    h = 1 / (np.sqrt(k * twoa / np.pi) * 2 / 3 - beta)
    q = 2 * np.pi / ((k ** 2) * s)
    qn = q ** n

    if g < f_lim:
        alpha = h / f_lim - 1
        xn = (h - alpha * g) ** n
    else:
        xn = g ** n
    
    rad = (xn + qn) ** (-1 / n)

    return rad

def shear(f, rho, e, sigma, dim):
    omega = 2 * np.pi * f

    chi = ((1 + sigma) / (0.87 * 1.12 * sigma)) ** 2

    x = (dim[2] ** 2) / 12
    qp = e / (1 - sigma ** 2)

    c = -omega * omega
    b = c * (1 + 2 * chi / (1 - sigma)) * x
    a = x * qp / rho

    kbcor2 = (-b + np.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    kb2 = np.sqrt(-c / a)

    g = e / (2 * (1 + sigma))

    kt2 = -c * rho * chi / g
    kl2 = -c * rho / qp
    ks2 = kt2 + kl2

    asi = (1 + x * (kbcor2 * kt2 / kl2 - kt2)) ** 2
    bsi = 1 - x * kt2 + kbcor2 * ks2 / (kb2 ** 2)
    csi = np.sqrt(1 - x * kt2 + (ks2 ** 2) / (4 * (kb2 ** 2)))

    out = asi / (bsi * csi)

    return out

def calc_radfree(f, fc, dim, c0 = 343):
    l1 = max(dim[0], dim[1])
    l2 = min(dim[0], dim[1])

    sig1 = 1 / (np.sqrt(1 - fc / f)) if f > fc else 2
    sig2 = 4 * l1 * l2 * ((f / c0) ** 2)
    sig3 = np.sqrt((2 * np.pi * f * (l1 + l2)) / (16 * c0))

    f11 = calc_f11(fc, dim, c0)

    if f11 <= (0.5 * fc):
        if f >= fc:    
            sig = sig1
        else:
            lamb = np.sqrt(f / fc)
            
            d1 = ((1 - lamb ** 2) * np.log((1 + lamb) / (1 - lamb)) + 2 * lamb) / (4 * (np.pi ** 2) * ((1 - lamb ** 2) ** 1.5))
            d2 = 0 if f > (0.5 * fc) else (8 * (c0 ** 2) * (1 - 2 * (lamb ** 2))) / ((fc ** 2) * (np.pi ** 4) * l1 * l2 * lamb * np.sqrt(1 - (lamb ** 2)))
            
            sig = ((2 * (l1 + l2)) / (l1 * l2)) * (c0 / fc) * d1 + d2
    
        if f < f11 and f11 < (0.5 * fc) and sig > sig2:
            sig = sig2

    else:
        if f < fc and sig2 < sig3:
            sig = sig2
        elif f > fc and sig1 < sig3:
            sig = sig1
        else:
            sig = sig3

    if sig > 2:
        sig = 2

    return sig

def calc_radforced(f, dim, c0 = 343):
    l1 = max(dim[0], dim[1])
    l2 = min(dim[0], dim[1])
    k0 = (2 * np.pi * f ) / c0

    lamb = -0.964 - (0.5 + l2 / (np.pi * l1)) * np.log(l2 / l1) + (5 * l2) / (2 * np.pi * l1) - 1 / (4 * np.pi * l1 * l2 * (k0 ** 2))

    sf = 0.5 * (np.log(k0 * np.sqrt(l1 * l2)) - lamb)

    return sf


t = 0.01
D = 0.1
r = 0.01
P = 160000
M = 5200000

def sig_nom():
    sig_nominal = P / (t*(D - 2*r))
    return sig_nominal
a = sig_nom()
print('sig_nom = ', a)


def k_theoretical():
    k = 3 - 3.13 * (2 *r / D) + 3.66 * (2*r / D) ** 2 - 1.53 * (2* r / D) ** 3
    return k
b = k_theoretical()
print('k_theoretical = ', b)

    # from 1.1

sig_max_low = 4.974e8
sig_max_mid = 5.017e8
sig_max_high = 5.033e8

k_low = sig_max_low/a
k_mid = sig_max_mid/a
k_high = sig_max_high/a

print(k_low, k_mid, k_high)

    #   from 1.2

sig_max_low_hole = 5.583e9
sig_max_mid_hole = 2.9522e9
sig_max_high_hole = 1.513e9

sig_max_low_plate = 3.118e11
sig_max_mid_plate = 3.124e11
sig_max_high_plate = 3.127e11

def sig_nom_hole():
    sig_nominal = (12*M*r)/(t*(D**3-(2 * r)**3))
    return sig_nominal

aa = sig_nom_hole()

print(aa)

def sig_nom_plate():
    sig_nominal = (6*M*D)/(t*(D**3-(2*r)**3))
    return sig_nominal

ab= sig_nom_plate()
print(ab)

k1 = sig_max_high_hole/aa
k2 = sig_max_high_plate/ab

print(k1, k2)
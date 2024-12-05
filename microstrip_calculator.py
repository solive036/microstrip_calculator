import numpy as np


### Microstrip width given characteristic impedance
def line_width(substrate_height, epsilon, z0):
    A = (z0/60)*np.sqrt((epsilon+1)/2)+((epsilon-1)/(epsilon+1))*(.23 + (.11/epsilon))
    wh = (8*np.e**A)/(np.e**(2*A)-2)
    line_width = wh * substrate_height
    return line_width

def line_impedance(zi, zl):
    return np.sqrt(zi*zl)

### Compute dimensions of microstrip patch
def patch_dimensions(frequency, epsilon, substrate_height):
    pw = patch_width(frequency, epsilon)
    eps_eff = epsilon_eff(epsilon, pw, substrate_height)
    pl = patch_length(frequency, eps_eff, pw, substrate_height)
    patch_impedance = patch_edge_impedance(pl, pw, epsilon)
    return [pw, pl, patch_impedance]

def patch_width(frequency, epsilon_r):
    w = ((3e8)/(2*frequency))*np.sqrt(2/(epsilon_r+1))
    return w

def epsilon_eff(epsilon_r, width, substrate_height):
    if (width/substrate_height) > 1:
        eps_eff = ((epsilon_r+1)/(2))+(((epsilon_r-1)/(2))*(1+12*(substrate_height/width))**(-1/2))
    else:
        eps_eff = ((epsilon_r+1)/2)+((epsilon_r-1)/2)*((1+12*(substrate_height/width))**(-1/2)+(0.04)*((1-(width/substrate_height)**2)))

    return eps_eff

def patch_length(frequency, eps_eff, width, substrate_height):
    L_eff = (3e8)/(2*frequency*np.sqrt(eps_eff))
    delta_L = (0.412*substrate_height)*(((eps_eff+0.3)*((width/substrate_height+0.264)))/((eps_eff-0.258)*(width/substrate_height+0.8)))
    L = L_eff - (2*delta_L)
    return L

def patch_edge_impedance(L, W, epsilon_r):
    Z_A = 90*((epsilon_r**2)/(epsilon_r-1))*((L/W)**2)
    return Z_A

def to_mm(num):
    num = round(num, 5)
    return num/1e-3


try:

    epsilon = float(input('Enter epsilon of substrate: '))
    substrate_height = float(input('Enter substrate height (mm): '))
    substrate_height = substrate_height*1e-3
    frequency = float(input('Enter Frequency (GHz): '))
    print('\n')

    while True:
        choice = int(input('1.patch dimensions, 2.microstrip width, 3.quarter wave transformer (ctrl C to quit): '))

        if choice == 1:
            PL, PW, zp = patch_dimensions(frequency, epsilon, substrate_height)
            print('\n')
            print('Patch width (mm): ', to_mm(PW))
            print('Patch length (mm): ', to_mm(PL))
            print('Patch edge impedance (ohms): ', zp)
            print('\n')

        elif choice == 2:
            print('\n')
            z0 = float(input('Enter characteristic impedance: '))
            LW = to_mm(line_width(substrate_height, epsilon, z0))
            print(str(z0) + 'ohm microstrip line width (mm): ' + str(LW))
            print('\n')

        elif choice == 3:
            zi = float(input('Enter input impedance: '))
            zl = float(input('Enter load impedance: '))
            z0 = line_impedance(zi, zl)
            LW = line_width(substrate_height, epsilon, z0)
            print('Microstrip line width:  ', to_mm(LW))

        else:
            print('Invalid input')

except KeyboardInterrupt:
    print('Exiting')
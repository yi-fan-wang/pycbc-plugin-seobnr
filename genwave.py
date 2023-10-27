import numpy as np
import lal
from pycbc.types import TimeSeries
from pyseobnr.generate_waveform import generate_modes_opt

def Ylm(l: int, m: int, theta: float, phi: float) -> float:
    """Get the spin-2 weighter spherical harmonics

    Args:
        l (int): ell
        m (int): m
        theta (float): inclination angle
        phi (float): azimuthal angle

    Returns:
        float: The value of the Ylm
    """
    return lal.SpinWeightedSphericalHarmonic(theta, phi, -2, l, m)


def combine_modes(
    iota: float, phi: float, modes_dict
):
    """Combine modes to compute the waveform polarizations in the direction
    (iota,np.pi/2-phi)

    Args:
        iota (float): Inclination angle (rad)
        phi (float): Azimuthal angle(rad)
        modes_dict (Dict): Dictionary containing the modes, either time of frequency-domain

    Returns:
        np.array: Waveform in the given direction
    """
    sm = 0.0
    for key in modes_dict.keys():
        #print(key)
        ell, m = [int(x) for x in key.split(",")]
        sm += Ylm(ell, m, iota, np.pi / 2 - phi) * modes_dict[key]
    return np.real(sm), -np.imag(sm)

def timeMtoSec(timeM, M):
    return timeM * M * lal.MTSUN_SI

def HztoOmegainvM(Hz, M):
    return np.pi * Hz * lal.MTSUN_SI * M

def ampNRtoPhysicalTD(ampNR, M, distance):
    return ampNR * (lal.C_SI * M *lal.MTSUN_SI)/distance

def genwave(**kwargs):
    '''PyCBC waveform generator for SEOBNRv5EHM
    '''

    q = kwargs['mass1']/kwargs['mass2']
    M_tot = kwargs['mass1'] + kwargs['mass2']
    chi_1 = [kwargs['spin1x'], kwargs['spin1y'], kwargs['spin1z']]
    chi_2 = [kwargs['spin2x'], kwargs['spin2y'], kwargs['spin2z']]
    eccentricity = kwargs['eccentricity']
    distance = 1e6 * lal.PC_SI * kwargs['distance']
    delta_t = kwargs['delta_t']
    rel_anomaly = kwargs['rel_anomaly']
    iota = kwargs['inclination']
    phi_angle = kwargs['coa_phase']
    omega0 = HztoOmegainvM(kwargs['f_lower'], M_tot)

    #sanity checks
    assert chi_1[0] == 0 and chi_1[1] == 0 and chi_2[0] == 0 and chi_2[1] == 0, \
                    "Invalid spin! SEOBNRv5E only supports aligned spin!"
    assert eccentricity >=0 and eccentricity <=1, \
                    "Invalid eccentricity! SEOBNRv5E only supports eccentricity in [0,1]"
    
    omega_start = omega0
    return_modes = [(2,2)]
    settings = {
        'M':M_tot,
        'dt':delta_t,
        "mode_factorization":4, 
        "x_prescription":"xAvg", 
        'return_modes':return_modes,
        'EccIC':0, #then omega0 corresponds to the initial instantaneous angular frequency. 
    }

    # SEOBNRv5EHM waveform evaluation
    time, hlm = generate_modes_opt(q, chi_1[2], chi_2[2], omega0, omega_start, eccentricity, 
    rel_anomaly, approximant="SEOBNRv5EHM", RRForce='Ecc', settings=settings)

    # Compute the negative m modes (aligned-spin)
    hlm_new = {}
    for key in hlm:
        ell, m = key.split(',')
        hlm_new[ell + ',-' + m] = (-1)**int(ell) * np.conj(hlm[key])

    hlm = hlm | hlm_new

    # Get the plus and cross polarizations (in geometric units) by adding all the modes
    hp_NR, hc_NR = combine_modes(iota, phi_angle, hlm)

    # Convert to SI units
    t_s = timeMtoSec(time, M_tot)
    hp = ampNRtoPhysicalTD(hp_NR, M_tot, distance)
    hc = ampNRtoPhysicalTD(hc_NR, M_tot, distance)

    # Build the TimeSeries format
    hpt = TimeSeries(hp, delta_t=delta_t, epoch=t_s[0])
    hct = TimeSeries(hc, delta_t=delta_t, epoch=t_s[0])

    return hpt,hct
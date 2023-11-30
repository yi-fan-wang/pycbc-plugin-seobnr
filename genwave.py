import numpy as np
import lal
from pycbc.types import TimeSeries
from pycbc.waveform.utils import taper_timeseries
from pyseobnr.generate_waveform import generate_modes_opt


def Ylm(l: int, m: int, theta: float, phi: float) -> float:
    """Get the spin-2 weighted spherical harmonics

    Args:
        l (int): ell
        m (int): m
        theta (float): inclination angle
        phi (float): azimuthal angle

    Returns:
        float: The value of the Ylm
    """
    return lal.SpinWeightedSphericalHarmonic(theta, phi, -2, l, m)


def combine_modes(iota: float, phi: float, modes_dict):
    """Combine modes to compute the waveform polarizations in the direction
    (iota,np.pi/2-phi)

    Args:
        iota (float): Inclination angle (rad)
        phi (float): Azimuthal angle(rad)
        modes_dict (Dict): Dictionary containing the modes, either time of frequency-domain

    Returns:
        np.array: Waveform in the given direction
    """
    sm = 0.0 #sm = h_+ - ih_x
    for key in modes_dict.keys():
        #print(key)
        ell, m = [int(x) for x in key.split(",")]
        sm += Ylm(ell, m, iota, np.pi / 2 - phi) * modes_dict[key]
    return np.real(sm), -np.imag(sm)

def timeMtoSec(timeM, M):
    return timeM * M * lal.MTSUN_SI

def HztoOmegainvM(Hz, M):
    '''Convert GW frequency to Omega measured by unit of 1/M
    '''
    return np.pi * Hz * lal.MTSUN_SI * M

def ampNRtoPhysicalTD(ampNR, M, distance):
    return ampNR * (lal.C_SI * M *lal.MTSUN_SI)/distance

def genseob_td(**kwargs):
    '''PyCBC waveform generator for SEOBNRv5E
    '''
    if kwargs['mass1'] < kwargs['mass2']:
        #swap index 1 and 2 for mass and spinz
        mass1 = kwargs['mass2']
        mass2 = kwargs['mass1']
        spin1z = kwargs['spin2z']
        spin2z = kwargs['spin1z']
        #no need to swap spinx and spiny cause they will be asserted to 0
    else:
        mass1 = kwargs['mass1']
        mass2 = kwargs['mass2']
        spin1z = kwargs['spin1z']
        spin2z = kwargs['spin2z']

    q = mass1 / mass2
    M_tot = mass1 + mass2
    chi_1 = [kwargs['spin1x'], kwargs['spin1y'], spin1z]
    chi_2 = [kwargs['spin2x'], kwargs['spin2y'], spin2z]
    
    eccentricity = kwargs['eccentricity']
    rel_anomaly = kwargs['rel_anomaly']
    
    delta_t = kwargs['delta_t']
    distance = 1e6 * lal.PC_SI * kwargs['distance']
    iota = kwargs['inclination']
    phi_angle = kwargs['coa_phase']
    #initial orbital angular frequency in unit of inverse M
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
    time, hlm = generate_modes_opt(q, chi_1[2], chi_2[2], 
        omega_start, omega0, #Omega_start, Omega_ref
        eccentricity, rel_anomaly, 
        approximant="SEOBNRv5EHM", RRForce='Ecc', settings=settings)

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

def genseob_fd(**kwargs):
    kwargs['delta_t'] = 1.0 / 2048
    hp, hc = genseob_td(**kwargs)

    # Resize to the right duration
    tsamples = int(1.0 / kwargs['delta_f'] / kwargs['delta_t'])

    if tsamples < len(hp):
        raise ValueError("The frequency spacing (df = {}) is too low to "
                         "generate the {} approximant from the time "
                         "domain".format(kwargs['delta_f'], kwargs['approximant']))

    hp.resize(tsamples)
    hc.resize(tsamples)

    hp = taper_timeseries(hp,'TAPER_START')
    hc = taper_timeseries(hc,'TAPER_START')

    # avoid wraparound
    hp = hp.to_frequencyseries().cyclic_time_shift(hp.start_time)
    hc = hc.to_frequencyseries().cyclic_time_shift(hc.start_time)
    return hp, hc
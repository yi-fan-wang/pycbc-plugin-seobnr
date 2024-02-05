import numpy as np
import lal
from pycbc.types import TimeSeries
from pycbc.waveform.utils import taper_timeseries
from pyseobnr.generate_waveform import GenerateWaveform

def genseob_td(**kwargs):
    '''PyCBC waveform generator for SEOBNRv5E
    '''
       
    parameters = {"mass1": kwargs["mass1"],
                  "mass2": kwargs["mass2"],
                  "spin1x": kwargs["spin1x"],
                  "spin1y": kwargs["spin1y"],
                  "spin1z": kwargs["spin1z"],
                  "spin2x": kwargs["spin2x"],
                  "spin2y": kwargs["spin2y"],
                  "spin2z": kwargs['spin2z'],
    
                  "distance": kwargs['distance'],
                  "inclination": kwargs["inclination"],
                
                  "phi_ref": kwargs["coa_phase"],
                  "f22_start": kwargs["f_lower"],
                  #"f_ref": kwargs["f_ref"],
                  "deltaT": kwargs['delta_t'],
                  "ModeArray": [(2,2)],
                             #[(2,2), (2,1), (3,2), (3,3), (4,3), (4,4), (5,5)]
                             # Specify which modes are to be returned

                  "rel_anomaly": kwargs['rel_anomaly'],
                  "eccentricity": kwargs['eccentricity'],
                  "approximant": "SEOBNRv5EHM",
                  
                  "postadiabatic": False,
                  "RRFroce": "Ecc",
                  "EccIC": 1, # EccIC = 0 for instantaneous initial orbital frequency
                             # EccIC = 1 for orbit-averaged initial orbital frequency
                  }
    waveform = GenerateWaveform(parameters)
    h_plus, h_cross = waveform.generate_td_polarizations()

    # Build the TimeSeries format
    hp = TimeSeries(h_plus.data.data, delta_t=h_plus.deltaT, epoch=h_plus.epoch)
    hc = TimeSeries(h_cross.data.data, delta_t=h_cross.deltaT, epoch=h_cross.epoch)

    return hp,hc

def genseob_fd(**kwargs):
    kwargs['delta_t'] = 1.0 / kwargs['f_final'] / 2
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
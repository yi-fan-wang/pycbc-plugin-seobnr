import numpy as np
from pycbc.types import TimeSeries
from pycbc.waveform.utils import taper_timeseries
from pyseobnr.generate_waveform import GenerateWaveform

def gen_seobnrv5ehm_td(**p):
    '''PyCBC waveform generator for SEOBNRv5E

    Parameters
    ----------
    dict: p
        A dictionary of parameters used by pycbc.waveform.get_td_waveform

    Returns
    -------
    hp: Array
        The plus polarization of the waveform in time domain
    hc: Array
        The cross polarization of the waveform in time domain
    """
    '''

    p.update({
        "rel_anomaly": p["rel_anomaly"], # relativity anomaly,  needed for eccentric waveform
        "phi_ref": p["coa_phase"], # reference phase needed by SEOBNRv5
        "f22_start": p["f_lower"], # starting frequency
        "f_ref": p["f_lower"],     # reference frequency
        "deltaT": p["delta_t"],    
        "ModeArray": [(2,2)],      # only consider (2,2) mode
        "postadiabatic": False     # turn off postadiabatic correction
        })

    waveform = GenerateWaveform(p)
    hp, hc = waveform.generate_td_polarizations()

    # Build the PyCBC TimeSeries format
    hp = TimeSeries(hp.data.data[:], delta_t=hp.deltaT, epoch=hp.epoch)
    hc = TimeSeries(hc.data.data[:], delta_t=hc.deltaT, epoch=hc.epoch)

    return hp,hc

def gen_seobnrv5ehm_fd(**kwargs):
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
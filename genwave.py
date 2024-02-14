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

    # Some waveform input parameters from PyCBC have the same naming 
    # conventions as PySEOBNR, thus they can be directly inherited. 
    # We only update the settings used uniquely by PySEOBNR
    p.update({
        "approximant": "SEOBNRv5EHM", # I call it "SEOBNRv5E" in PyCBC 
        "ModeArray": [(2,2)],      # only consider (2,2) mode
        "rel_anomaly": p["rel_anomaly"], # relativity anomaly,  needed for eccentric waveform
        "phi_ref": p["coa_phase"], # reference phase needed by SEOBNRv5
        "f22_start": p["f_lower"], # starting frequency
        "f_ref": p["f_lower"],     # reference frequency
        "deltaT": p["delta_t"],    
        "postadiabatic": False ,   # turn off postadiabatic correction
        "h_0": 1.0,                # initial time step in the integration of the ODEs.
        "lmax_nyquist": 1          # maximum L to be checked against Nyquist frequency
        })

    waveform = GenerateWaveform(p)
    hp, hc = waveform.generate_td_polarizations()

    # Build the PyCBC TimeSeries format
    hp = TimeSeries(hp.data.data[:], delta_t=hp.deltaT, epoch=hp.epoch)
    hc = TimeSeries(hc.data.data[:], delta_t=hc.deltaT, epoch=hc.epoch)

    return hp,hc

def length_in_time(**kwds):
    from pycbc.waveform.waveform import get_waveform_filter_length_in_time
    if kwds['approximant'] == 'SEOBNRv5E':
        kwds['approximant'] = "SEOBNRv5_ROM" # Approximate the length of SEOBNRv5E by SEOBNRv5_ROM
    return get_waveform_filter_length_in_time(**kwds)
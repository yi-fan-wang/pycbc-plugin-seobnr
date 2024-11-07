import numpy as np
from pycbc.types import TimeSeries, FrequencySeries
#from pycbc.waveform.utils import taper_timeseries
from pyseobnr.generate_waveform import GenerateWaveform

def gen_seobnrv5e_td(**p):
    p.update({
        "approximant": "SEOBNRv5EHM", # I call it "SEOBNRv5E" in PyCBC 
        "ModeArray": [(2,2)],      # only consider (2,2) mode
        "rel_anomaly": p["rel_anomaly"], # relativity anomaly,  needed for eccentric waveform
        "phi_ref": p["coa_phase"], # reference phase needed by SEOBNRv5
        "f22_start": p["f_lower"], # starting frequency
        "f_ref": p["f_lower"],     # reference frequency
        "deltaT": p["delta_t"],    
        #"postadiabatic": False ,   # turn off postadiabatic correction, 
                                   # default is False in SEOBNRv5EHM
        #"h_0": 1.0,                # initial time step in the integration of the ODEs. 
                                    # Default Value is 1.0
        "lmax_nyquist": 1          # maximum L to be checked against Nyquist frequency
        })

    waveform = GenerateWaveform(p)
    hp, hc = waveform.generate_td_polarizations_conditioned_1()

    # Build the PyCBC TimeSeries format
    hp = TimeSeries(hp.data.data[:], delta_t=hp.deltaT, epoch=hp.epoch)
    hc = TimeSeries(hc.data.data[:], delta_t=hc.deltaT, epoch=hc.epoch)

    return hp,hc

def gen_seobnrv5e_fd(**p):
    p.update({
        "approximant": "SEOBNRv5EHM",
        "ModeArray": [(2,2)],      # only consider (2,2) mode
        "rel_anomaly": p["rel_anomaly"] if "rel_anomaly" in p else 0, # relativity anomaly,  needed for eccentric waveform
        "phi_ref": p["coa_phase"], # reference phase needed by SEOBNRv5
        "f22_start": p["f_lower"], # starting frequency
        "f_ref": p["f_lower"],     # reference frequency
        "deltaF": p["delta_f"],    
        #"postadiabatic": False ,   # turn off postadiabatic correction, 
                                   # default is False in SEOBNRv5EHM
        #"h_0": 1.0,                # initial time step in the integration of the ODEs. 
                                    # Default Value is 1.0
        "lmax_nyquist": 1          # maximum L to be checked against Nyquist frequency
        })

    waveform = GenerateWaveform(p)
    hp, hc, template_duration = waveform.generate_fd_polarizations()

    # Build the PyCBC TimeSeries format
    hp_pycbc = FrequencySeries(hp.data.data[:], delta_f=hp.deltaF, epoch=hp.epoch)
    hc_pycbc = FrequencySeries(hc.data.data[:], delta_f=hc.deltaF, epoch=hp.epoch)
    
    hp_pycbc.eob_template_duration = template_duration
    hc_pycbc.eob_template_duration = template_duration

    return hp_pycbc,hc_pycbc

def gen_seobnrv5ehm_fd(**p):
    p.update({
        "approximant": "SEOBNRv5EHM",
        "rel_anomaly": p["rel_anomaly"] if "rel_anomaly" in p else 0, # relativity anomaly,  needed for eccentric waveform
        "phi_ref": p["coa_phase"], # reference phase needed by SEOBNRv5
        "f22_start": p["f_lower"], # starting frequency
        "f_ref": p["f_lower"],     # reference frequency
        "deltaF": p["delta_f"],    
        })

    waveform = GenerateWaveform(p)
    hp, hc, template_duration = waveform.generate_fd_polarizations()

    # Build the PyCBC TimeSeries format
    hp_pycbc = FrequencySeries(hp.data.data[:], delta_f=hp.deltaF, epoch=hp.epoch)
    hc_pycbc = FrequencySeries(hc.data.data[:], delta_f=hc.deltaF, epoch=hp.epoch)
    
    hp_pycbc.eob_template_duration = template_duration
    hc_pycbc.eob_template_duration = template_duration

    return hp_pycbc,hc_pycbc

def seobnrv5phm_length_in_time(**kwds):
    from pycbc.waveform.waveform import get_hm_length_in_time
    return get_hm_length_in_time('SEOBNRv5', 5, **kwds)
  
#def seobnrv5e_length_in_time(**kwds):
#    from pycbc.waveform.waveform import get_waveform_filter_length_in_time
#    if "approximant" in kwds:
#        kwds.pop("approximant")
#    return get_waveform_filter_length_in_time(approximant='SEOBNRv5_ROM', **kwds)

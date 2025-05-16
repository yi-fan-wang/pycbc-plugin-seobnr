import numpy as np
from pycbc.types import TimeSeries, FrequencySeries
from pyseobnr.generate_waveform import GenerateWaveform

def convert_pycbc_to_seobnr(domain, p_input):
    '''
    Convert PyCBC waveform parameters to pyseobnr conventions.
    '''
    p = p_input.copy()
    p["rel_anomaly"] = p.pop("rel_anomaly", 0) # relativity anomaly, needed for eccentric waveform
    p["phi_ref"] = p.pop("coa_phase") # reference phase needed by SEOBNRv5
    p["f22_start"] = p.pop("f_lower") # starting frequency
    p["f_ref"] = p["f22_start"]     # reference frequency, use starting frequency at the moment
    if domain == "frequency":
        p["deltaF"] = p.pop("delta_f")  # frequency spacing
    elif domain == 'time':
        p["deltaT"] = p.pop("delta_t")  # time spacing
    else:
        raise ValueError("domain must be 'frequency' or 'time'")
    return p

def base_seobnrv5e(highermode, domain, p_pycbc):
    '''
    Convert PyCBC waveform parameters to pyseobnr waveform parameters and 
    generate the waveform in frequency domain. Parameters are hardcoded to 
    only use SEOBNRv5EHM 's (2,2) mode and not check Nyquist frequency
    '''    
    p_eob = convert_pycbc_to_seobnr(domain, p_pycbc)
    p_eob["approximant"] = "SEOBNRv5EHM"
    if not highermode:
        p_eob["ModeArray"] = [(2,2)]
    p_eob["lmax_nyquist"] = 1
    waveform = GenerateWaveform(p_eob)

    if domain == "frequency":
        # generate the frequency domain waveform
        hp, hc, template_duration = waveform.generate_fd_polarizations()

        # Build the PyCBC TimeSeries format
        hp_pycbc = FrequencySeries(hp.data.data[:], delta_f = hp.deltaF, epoch = hp.epoch)
        hc_pycbc = FrequencySeries(hc.data.data[:], delta_f = hc.deltaF, epoch = hp.epoch)
        
        # Fix the pyseobnr convention to let peak time be at 0
        hp_pycbc = hp_pycbc.cyclic_time_shift(hp_pycbc.start_time + hp_pycbc.duration)
        hc_pycbc = hc_pycbc.cyclic_time_shift(hc_pycbc.start_time + hc_pycbc.duration)

        hp_pycbc.eob_template_duration = template_duration
        hc_pycbc.eob_template_duration = template_duration
    elif domain == "time":
        # generate the time domain waveform with the start tapered
        hp, hc = waveform.generate_td_polarizations_conditioned_1()

        # Build the PyCBC TimeSeries format
        hp_pycbc = TimeSeries(hp.data.data[:], delta_t = hp.deltaT, epoch = hp.epoch)
        hc_pycbc = TimeSeries(hc.data.data[:], delta_t = hc.deltaT, epoch = hc.epoch)
    else:
        raise ValueError("domain must be 'frequency' or 'time'")

    return hp_pycbc,hc_pycbc

def gen_seobnrv5e_td(**p):
    return base_seobnrv5e(False, "time", p)

def gen_seobnrv5e_fd(**p):
    return base_seobnrv5e(False, "frequency", p)

def gen_seobnrv5ehm_td(**p):
    return base_seobnrv5e(True, "time", p)

def gen_seobnrv5ehm_fd(**p):
    return base_seobnrv5e(True, "frequency", p)

def seobnrv5phm_length_in_time(**kwds):
    from pycbc.waveform.waveform import get_hm_length_in_time
    return get_hm_length_in_time('SEOBNRv5', 5, **kwds)
  
#def seobnrv5e_length_in_time(**kwds):
#    from pycbc.waveform.waveform import get_waveform_filter_length_in_time
#    if "approximant" in kwds:
#        kwds.pop("approximant")
#    return get_waveform_filter_length_in_time(approximant='SEOBNRv5_ROM', **kwds)

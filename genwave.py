import numpy as np
from pycbc.types import TimeSeries, FrequencySeries
from pyseobnr.generate_waveform import GenerateWaveform
from pycbc.waveform import FailedWaveformError

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

def base_seobnrv5e(highermode, domain, p_pycbc, taper=True, model="SEOBNRv5EHM"):
    '''
    Convert PyCBC waveform parameters to pyseobnr waveform parameters and
    generate the waveform in frequency domain. Parameters are hardcoded to
    only use the eccentric EHM model's (2,2) mode (unless highermode) and
    not check the Nyquist frequency. `model` selects the pyseobnr
    approximant, e.g. "SEOBNRv5EHM" or "SEOBNRv6EHM" (the latter requires a
    pyseobnr build that provides the v6 model).
    '''
    p_eob = convert_pycbc_to_seobnr(domain, p_pycbc)
    p_eob["approximant"] = model
    if not highermode:
        p_eob["ModeArray"] = [(2,2)]
    p_eob["lmax_nyquist"] = 1
    waveform = GenerateWaveform(p_eob)

    try:
        if domain == "frequency":
            # generate the frequency domain waveform
            hp, hc = waveform.generate_fd_polarizations()

            # Build the PyCBC TimeSeries format
            hp_pycbc = FrequencySeries(hp.data.data[:], delta_f = hp.deltaF, epoch = hp.epoch)
            hc_pycbc = FrequencySeries(hc.data.data[:], delta_f = hc.deltaF, epoch = hp.epoch)
            
            # Fix the pyseobnr convention to let peak time be at 0
            hp_pycbc = hp_pycbc.cyclic_time_shift(hp_pycbc.start_time + hp_pycbc.duration)
            hc_pycbc = hc_pycbc.cyclic_time_shift(hc_pycbc.start_time + hc_pycbc.duration)
        elif domain == "time":
            if taper:
            # generate the time domain waveform with the start tapered
                hp, hc = waveform.generate_td_polarizations_conditioned_1()
            else:
                hp, hc = waveform.generate_td_polarizations()

            # Build the PyCBC TimeSeries format
            hp_pycbc = TimeSeries(hp.data.data[:], delta_t = hp.deltaT, epoch = hp.epoch)
            hc_pycbc = TimeSeries(hc.data.data[:], delta_t = hc.deltaT, epoch = hc.epoch)
        else:
            raise FailedWaveformError("domain must be 'frequency' or 'time'")

    except ValueError:
        name = model if highermode else model.replace("EHM", "E")
        raise FailedWaveformError("Failed to generate %s waveform in %s domain."
                                  % (name, domain))

    return hp_pycbc,hc_pycbc
    
def gen_seobnrv5e_tdtaper(**p):
    return base_seobnrv5e(False, "time", p, True)

def gen_seobnrv5e_td(**p):
    return base_seobnrv5e(False, "time", p, False)

def gen_seobnrv5e_fd(**p):
    return base_seobnrv5e(False, "frequency", p)

def gen_seobnrv5ehm_tdtaper(**p):
    return base_seobnrv5e(True, "time", p, True)

def gen_seobnrv5ehm_td(**p):
    return base_seobnrv5e(True, "time", p, False)

def gen_seobnrv5ehm_fd(**p):
    return base_seobnrv5e(True, "frequency", p)

def gen_seobnrv6e_tdtaper(**p):
    return base_seobnrv5e(False, "time", p, True, model="SEOBNRv6EHM")

def gen_seobnrv6e_td(**p):
    return base_seobnrv5e(False, "time", p, False, model="SEOBNRv6EHM")

def gen_seobnrv6e_fd(**p):
    return base_seobnrv5e(False, "frequency", p, model="SEOBNRv6EHM")

def seobnrv5phm_length_in_time(**kwds):
    from pycbc.waveform.waveform import get_hm_length_in_time
    return get_hm_length_in_time('SEOBNRv5', 5, **kwds)
  
#def seobnrv5e_length_in_time(**kwds):
#    from pycbc.waveform.waveform import get_waveform_filter_length_in_time
#    if "approximant" in kwds:
#        kwds.pop("approximant")
#    return get_waveform_filter_length_in_time(approximant='SEOBNRv5_ROM', **kwds)

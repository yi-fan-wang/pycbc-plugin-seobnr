# pycbc-plugin-seobnr
A pycbc waveform generation plugin for [pySEOBNR](https://git.ligo.org/waveforms/software/pyseobnr)

# To install
```
pip install .
```
# Instructions

We provide six waveform approximants for PyCBC by directly calling `pySEOBNR` and making custom conditions:
```
Time domain waveform:
 - SEOBNRv5E_tdtaper: 22 mode, start tapered
 - SEOBNRv5E_td: 22 mode
 - SEOBNRv5EHM_tdtaper: all available modes, start tapered
 - SEOBNRv5EHM_td: all available modes

Frequency domain waveform:
 - SEOBNRv5E: 22 mode
 - SEOBNRv5EHM: all available modes
```

To call the waveform approximants in PyCBC:
```
from pycbc import waveform
hp, hc = waveform.get_fd_waveform(approximant="SEOBNRv5EHM",mass1=30,mass2=30,eccentricit=0.3,rel_anomaly=1,delta_f = 1/4,f_lower=20)
```

```
from pycbc import waveform
hp_td, hc_td = waveform.get_td_waveform(approximant="SEOBNRv5EHM_td",mass1=30,mass2=30,eccentricit=0.3,rel_anomaly=1,delta_t = 1/1024,f_lower=20)
```

# Reference:
The `SEOBNRv5E` was used in the following work to search for the eccentric binary black holes from the LIGO-Virgo O3 data release.

 - [Search for gravitational waves from eccentric binary black holes with an effective-one-body template by Yi-Fan Wang and Alex Nitz](https://arxiv.org/abs/2508.05018)



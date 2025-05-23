"""
setup.py file to hook up pyseobnr with pycbc waveform plugin
"""

from setuptools import Extension, setup, Command, find_packages

VERSION = '0.1'

setup (
    name = 'pycbc-seobnr',
    version = VERSION,
    description = 'A waveform plugin for PyCBC for pySEOBNR',
    author = 'Yifan Wang',
    author_email = 'yifan.wang@aei.mpg.de',
    url = 'https://github.com/yi-fan-wang/pycbc-plugin-seobnr',
    keywords = ['effective one body', 'gravitational waves', 'pycbc'],
    packages = find_packages(),
    py_modules = ['genwave'],
    #package_dir = {'':'src'},
    #package_dir={'PyTGR': 'src'},
    entry_points = {"pycbc.waveform.td":["SEOBNRv5E_tdtaper = genwave:gen_seobnrv5e_td",
                                         "SEOBNRv5EHM_tdtaper = genwave:gen_seobnrv5ehm_td"],
                    "pycbc.waveform.fd":["SEOBNRv5E = genwave:gen_seobnrv5e_fd",
                                         "SEOBNRv5EHM = genwave:gen_seobnrv5ehm_fd"],
                    "pycbc.waveform.length":["SEOBNRv5PHM = genwave:seobnrv5phm_length_in_time"]
                    },
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
)

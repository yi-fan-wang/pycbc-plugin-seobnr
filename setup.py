"""
setup.py file to hook up pyseobnr with pycbc waveform plugin
"""

from setuptools import Extension, setup, Command, find_packages

VERSION = '0.0'

setup (
    name = 'pycbc-seobnr',
    version = VERSION,
    description = 'A waveform plugin for PyCBC for pySEOBNR',
    author = 'Yifan Wang',
    author_email = 'yifan.wang@aei.mpg.de',
    url = 'https://github.com/yi-fan-wang/pycbc-plugin-seobnr',
    #download_url = 'https://github.com/gwastro/revchirp/tarball/v%s' % VERSION,
    keywords = ['effective one body', 'gravitational waves', 'pycbc'],
    packages = find_packages(),
    py_modules = ['genwave'],
    #package_dir = {'':'src'},
    #package_dir={'PyTGR': 'src'},
    entry_points = {"pycbc.waveform.td":["SEOBNRv5E_tdtaper = genwave:gen_seobnrv5e_td",
                                         "SEOBNRv5PHM = genwave:gen_seobnrv5phm_td"],
                    "pycbc.waveform.fd":["SEOBNRv5E = genwave:gen_seobnrv5e_fd"],
                    "pycbc.waveform.length":["SEOBNRv5PHM = genwave:seobnrv5phm_length_in_time"]
                    },
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
)

"""
setup.py file for testing birefringence pycbc waveform plugin package
"""

from setuptools import Extension, setup, Command, find_packages

VERSION = '0.0'

setup (
    name = 'pycbc-seobnr',
    version = VERSION,
    description = 'A waveform plugin for PyCBC for pySEOBNR',
    author = 'Yifan Wang',
    author_email = 'yifan.wang@aei.mpg.de',
    url = 'https://github.com/yi-fan-wang/TestingGR_with_Gravwaves',
    #download_url = 'https://github.com/gwastro/revchirp/tarball/v%s' % VERSION,
    keywords = ['effective one body', 'gravitational waves', 'pycbc'],
    packages = find_packages(),
    py_modules = ['genwave'],
    #package_dir = {'':'src'},
    #package_dir={'PyTGR': 'src'},
    entry_points = {"pycbc.waveform.td":["SEOBNRv5E = genwave:genseob_td"],
                    "pycbc.waveform.fd":["SEOBNRv5E = genwave:genseob_fd"]},
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

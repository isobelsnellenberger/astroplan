"""
This file contains functions that configure py.test like astropy but with
additions for astroplan.  Py.test looks for specially-named functions
(like  ``pytest_configure``) and uses those to configure itself.

Here, we want to keep the behavior of astropy while *adding* more for astroplan.
To do that, in the functions below, we first invoke the functions from astropy,
and then after that do things specific to astroplan.  But we also want astropy
functionality for any functions we have *not* overriden, so that's why the
``import *`` happens at the top.
"""
from astropy.tests.pytest_plugins import *

# also save a copy of the astropy hooks so we can use them below when
# overriding
from astropy.tests import pytest_plugins as astropy_pytest_plugins

import warnings
from .utils import _mock_remote_data, _unmock_remote_data
from .exceptions import AstroplanWarning

import os

# This is to figure out the affiliated package version, rather than
# using Astropy's
try:
    from .version import version
except ImportError:
    version = 'dev'

packagename = os.path.basename(os.path.dirname(__file__))
TESTED_VERSIONS[packagename] = version


# Comment out this line to avoid deprecation warnings being raised as
# exceptions
enable_deprecations_as_exceptions()

# Define list of packages for which to display version numbers in the test log
try:
    PYTEST_HEADER_MODULES['Astropy'] = 'astropy'
    PYTEST_HEADER_MODULES['pytz'] = 'pytz'
    PYTEST_HEADER_MODULES['pyephem'] = 'ephem'
    PYTEST_HEADER_MODULES['matplotlib'] = 'matplotlib'
    PYTEST_HEADER_MODULES['pytest-mpl'] = 'pytest_mpl'
    del PYTEST_HEADER_MODULES['h5py']
except KeyError:
    pass


def pytest_configure(config):
    if hasattr(astropy_pytest_plugins, 'pytest_configure'):
        # sure ought to be true right now, but always possible it will change in
        # future versions of astropy
        astropy_pytest_plugins.pytest_configure(config)

    # make sure astroplan warnings always appear so we can test when they show
    # up
    warnings.simplefilter('always', category=AstroplanWarning)

    # Activate remote data mocking if the `--remote-data` option isn't used:
    if (not config.getoption('remote_data') or
            config.getvalue('remote_data') == 'none'):
        _mock_remote_data()

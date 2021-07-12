'''
Trinomial: TRIvial aNOnyMIzAtion Library

Copyright
---------

Copyright (c) 2021 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

# Package metadata ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#  ╭────────────────────── Notice ── Notice ── Notice ─────────────────────╮
#  |    The following values are automatically updated at every release    |
#  |    by the Makefile. Manual changes to these values will be lost.      |
#  ╰────────────────────── Notice ── Notice ── Notice ─────────────────────╯

__version__     = '0.0.3'
__description__ = 'A simple name anonymization library'
__url__         = 'https://github.com/caltechlibrary/trinomial'
__author__      = 'Michael Hucka'
__email__       = 'mhucka@library.caltech.edu'
__license__     = 'BSD 3-clause'


# Exports.
# .............................................................................

from .trinomial import anon, set_unique_key


# Miscellaneous utilities.
# .............................................................................

def print_version():
    print(f'{__name__} version {__version__}')
    print(f'Authors: {__author__}')
    print(f'URL: {__url__}')
    print(f'License: {__license__}')

import os
import pytest
import sys
from   time import time

try:
    thisdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(thisdir, '..'))
except:
    sys.path.append('..')

import trinomial

def test_basic():
    trinomial.set_unique_key('x')
    assert trinomial.anon('foo@bar.com') == '55086f20ea'
    assert trinomial.anon('foo@bar.com') == '55086f20ea'

def test_repeat():
    trinomial.set_unique_key('x')
    assert trinomial.anon('foo@bar.com') == '55086f20ea'

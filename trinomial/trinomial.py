'''
trinomial.py: main code for Trinomial

Authors
-------

Michael Hucka <mhucka@library.caltech.edu>

Copyright
---------

Copyright (c) 2021 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

from hashlib import blake2b
import platform


# Internal variables and one-time computations.
# .............................................................................

def _key_for_host():
    key = None
    sys = platform.system().lower()

    # Our fallback aproach is uuid.getnode(). However, that's based on the
    # network hardware address of the host, and AFAIK it could change after a
    # reboot if the machine has multiple NICs.  So we try first to find a
    # more stable identifier for those systems where we know how to do it.
    if sys.startswith('darwin'):
        import json
        import re
        from subprocess import check_output, SubprocessError
        try:
            txt = check_output('ioreg -rd1 -c IOPlatformExpertDevice'.split())
            match = re.search(r'"IOPlatformUUID"\s+=\s+"([^"]+)', txt.decode())
            if match is not None:
                key = match.group(1)
            # Else, fall through.
        except SubprocessError as ex:
            pass
    elif sys.startswith('linux'):
        # dmidecode is not an option because we have to find something we can
        # use without being root.  Next best choice is this:
        try:
            with open('/var/lib/dbus/machine-id', 'r') as f:
                key = f.read().strip()
        except (OSError, IOError):
            pass
        # Some systems don't have dbus installed & the above will fail.  The
        # following should stay the same across reboots for normal (physical)
        # computers but will probably change on cloud-provisioned systems.
        try:
            with open('/etc/machine-id', 'r') as f:
                key = f.read().strip()
        except (OSError, IOError):
            pass
    elif sys.startswith('win'):
        import re
        from subprocess import check_output, SubprocessError
        # The following is based on a posting to Stack Overflow on 2019-10-16 by
        # user "Mitch McMabers" at https://stackoverflow.com/a/58416992/743730
        try:
            txt = check_output("wmic csproduct get uuid".split())
            # Attempt to extract the UUID from the command's result.
            match = re.search(r"\bUUID\b[\s\r\n]+([^\s\r\n]+)", txt.decode())
            if match is not None:
                value = match.group(1)
                if value is not None:
                    # Remove the surrounding whitespace (newlines, space, etc)
                    # & useless dashes etc, by only keeping hex (0-9 A-F) chars.
                    key = re.sub(r"[^0-9A-Fa-f]+", "", value)
        except SubprocessError as ex:
            pass

    if key:
        return key.encode()
    else:
        # OK, we have to use our fallback approach.
        import uuid
        return str(uuid.getnode()).encode()


_UNIQUE_KEY = _key_for_host()


# Exported functions.
# .............................................................................

def anon(text, length = 10):
    if text is None:
        return ''
    h = blake2b(digest_size = length, key = _UNIQUE_KEY)
    h.update(text.encode())
    # Hex digests produce strings of twice the length.  We truncate the
    # result to the desired length.  This doubles the number of possible
    # collisions compared to the unmodified Blake2b hash.  That actually
    # increases security for our purpose of obscuring the original value, but
    # also increases the risk of collisions compared to Blake2b.  However,
    # collision risk is measured in terms of bits in the final hash string,
    # according to 2^(n/2), where n is the number of bits.  A length of 10
    # hex digits is 40 bits => 2^(40/2) = 2^20 = 1,048,576 unique values.
    return h.hexdigest()[:length]


def set_unique_key(key):
    global _UNIQUE_KEY
    if type(key) is bytes:
        _UNIQUE_KEY = key
    else:
        try:
            _UNIQUE_KEY = str(key).encode()
        except (UnicodeDecodeError, AttributeError):
            pass

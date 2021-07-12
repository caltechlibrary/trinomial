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
    operating_system = platform.system().lower()

    # Our fallback is uuid.getnode(), but it's a poor choice for this, so first
    # try to find a more stable identifier for those systems where we know how.
    if operating_system.startswith('darwin'):
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
    elif operating_system.startswith('linux'):
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
    elif operating_system.startswith('win'):
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
        # We have to use the fallback. It's not a great solution: it uses the
        # MAC address of a NIC (which may change on reboot if a machine has
        # multiple network interfaces) and if it can't get the address, getnode
        # resorts to generating a random number.  Moreover, other machines on
        # the same network can learn the MAC address, which makes it poor for
        # privacy.  Despite all this, I haven't found a better fallback option.
        import uuid
        return str(uuid.getnode()).encode()


_UNIQUE_KEY = _key_for_host()


# Exported functions.
# .............................................................................

def anon(text, length = 10):
    '''Take "text" and transform it to a short string of hexadecimal digits.

    The transformation is based on hashing the original string in combination
    with a unique key derived from the computer on which Trinomial is used.
    To the degree possible, the transformation is consistent, such that the
    same input will always yield the same output.  This is guaranteed to be
    the case within a single run of the program calling this function; it
    should also be true from run to run as well, but on some systems, the
    unique key may change after a reboot, and this will change the output for
    a given input.  Virtual machines and cloud-provisioned systems, in
    particular, may suffer from this limitation.

    The unique key can be set explicitly using set_unique_key(...).

    The possibility of output collisions between two or more identical input
    values is low, but not zero.  The calculation of collisions for a hash
    function is based on the number of bits b in the hashed output value,
    according to the function 2^(b/2).  A hexadecimal character can encode 4
    bits, which means a hexadecimal string of length n is equal to n * 4 bits.
    This means that the Trinomial default length of 10 output characters
    gives a maximum of 2^(4*10/2) = 1,048,576 possible unique values.  In the
    author's opinion, this is reasonable for a situation such as (e.g.)
    anonymizing email addresses in the logs of a program at a small
    educational institution, but may be too low for other situations. Users
    may want to increase the `length` parameter to `anon` accordingly.
    '''

    global _UNIQUE_KEY
    if text is None:
        return ''
    hash = blake2b(digest_size = length, key = _UNIQUE_KEY)
    hash.update(text.encode())
    # Hex digests produce strings of twice the length.  We truncate the
    # result to the desired length.  This doubles the number of possible
    # collisions compared to the unmodified Blake2b hash.  That actually
    # increases security for our purpose of obscuring the original value, but
    # also increases the risk of collisions compared to Blake2b.  However,
    # collision risk is measured in terms of bits in the final hash string,
    # according to 2^(n/2), where n is the number of bits.  A length of 10
    # hex digits is 40 bits => 2^(40/2) = 2^20 = 1,048,576 unique values.
    return hash.hexdigest()[:length]


def set_unique_key(key):
    '''Reset the unique key used by anon(...) to a known value.

    Setting this value will mean that anon(...) will generate the same output
    for a given input on any host computer (instead of the goal, which is to
    generate a different output on different computers).  This is intended for
    testing and debugging.  Do not do this in production code.  Setting the
    value in your code makes it much easier for someone to try to reverse the
    process of producing the output.  The function `set_unique_key` is meant
    for testing and debugging.
    '''

    global _UNIQUE_KEY
    if type(key) is bytes:
        _UNIQUE_KEY = key
    else:
        try:
            _UNIQUE_KEY = str(key).encode()
        except (UnicodeDecodeError, AttributeError):
            pass

# Trinomial<img width="65em" align="right" src="https://github.com/caltechlibrary/trinomial/raw/main/.graphics/trinomial.png">

Trinomial is a simple Python library for performing a one-way transformation from a text string (such as a person's name or email address) to a short hexadecimal character sequence. The result can be used in place of the original string to hide a person's identity in log messages and similar situations.

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat-square)](https://choosealicense.com/licenses/bsd-3-clause)
[![Python](https://img.shields.io/badge/Python-3.8+-brightgreen.svg?style=flat-square)](https://www.python.org/downloads/release/python-380/)
[![Latest release](https://img.shields.io/github/v/release/caltechlibrary/trinomial.svg?style=flat-square&color=b44e88)](https://github.com/caltechlibrary/trinomial/releases)
[![DOI](https://img.shields.io/badge/dynamic/json.svg?label=DOI&style=flat-square&color=lightgray&query=$.metadata.doi&uri=https://data.caltech.edu/api/record/2030)](https://data.caltech.edu/records/2030)
[![PyPI](https://img.shields.io/pypi/v/trinomial.svg?style=flat-square&color=orange)](https://pypi.org/project/trinomial/)


## Table of contents

* [Introduction](#introduction)
* [Installation](#installation)
* [Usage](#usage)
* [Known issues and limitations](#known-issues-and-limitations)
* [Getting help](#getting-help)
* [Contributing](#contributing)
* [License](#license)
* [Authors and history](#authors-and-history)
* [Acknowledgments](#authors-and-acknowledgments)


## Introduction

If you want to preserve user's privacy in software applications, you need to avoid storing or printing user identities to the maximum extent possible. One of the situations in which user identities can leak is software logging or debugging messages. Even when stored only on servers in server logs, user identities are at risk of exposure to systems administrators, hackers, or the developers of the software. The challenge is that it's often important for debugging or other analysis to be able to recognize the same user in multiple messages even if we don't need to know their real identities. Thus, what we need is a way to tell user _A_ from user _B_, even if we don't care to know who _A_ and _B_ are in the real world.

Trinomial (_**tri**vial a**no**ny**mi**z**a**tion **l**ibrary_) is a Python package that can help keep users anonymous in such situations. It takes a string (such as an email address, or a name) and transforms it in a consistent way &ndash; the same input will always yield the same output &ndash; that is also **irreversible**: given only the output, it is impossible to determine the unique original input that produce it, even knowing Trinomial's source code. You can apply Trinomial to names in error messages in your application, and the names will be transformed to short strings of (essentially) random hexadecimal digits everywhere they appear.

Using Trinomial in code is simply a matter of calling a certain function when you want to print something that may be identifiable. Here is a hypothetical example:

```python
from trinomial import anon

# do some stuff ...

email = request.forms.get('email')
logging.info(f'got submission from user {anon(email)}')

# do some other stuff ...

logging.info(f'redirecting {anon(email)} to page /flowers')
```

Please be aware that this kind of approach **only offers pseudoanonymity at best**. It cannot protect against a number of other methods of breaking anonymity, such as analyzing correlations between information in your logs or reading IP addresses (if your logs also contain IP addresses).  Trinomial can help improve anonymity, but it cannot do everything alone. It is **not intended for sensitive applications, or legal requirements such as the GDPR,  HIPAA, or producing public data sets, or similar situations**.


## Installation

The instructions below assume you have a Python interpreter installed on your computer; if that's not the case, please first [install Python version 3](INSTALL-Python3.md) and familiarize yourself with running Python programs on your system.

On **Linux**, **macOS**, and **Windows** operating systems, you should be able to install `trinomial` with [`pip`](https://pip.pypa.io/en/stable/installing/).  To install `trinomial` from the [Python package repository (PyPI)](https://pypi.org), run the following command:
```
python3 -m pip install trinomial
```

As an alternative to getting it from [PyPI](https://pypi.org), you can use `pip` to install `trinomial` directly from GitHub, like this:
```sh
python3 -m pip install git+https://github.com/caltechlibrary/trinomial.git
```
 

## Usage

The main function provided by Trinomial is `anon`. It takes an input string of characters and returns a transformed, shorter string.

```python
>>> from trinomial import anon
>>> email = 'flower@example.com'
>>> anon(email)
'bcb403adb7'
```

The output of `anon` is a string of hexadecimal digits.  The function `anon` accepts an optional argument to control the length of the output string.  The default length is 10 hex digits.  (See the section on [Known issues and limitations](#known-issues-and-limitations) for more information about the implications of this.)

```python
>>> anon(email, length = 5)
'ed598'
```


### _Special functions_

Trinomial takes measures to increase anonymity beyond what would be obtained by simply hashing text strings.  One is that it computes hashes by incorporating a unique key derived from the identity of the computer on which it is running.  Thus, a given input to the `anon` function on two different computers will produce two different results. This is on purpose, so that someone can't take the output of `anon` and easily mount an offline brute-force [preimage attack](https://en.wikipedia.org/wiki/Preimage_attack) to guess what input produced that output _without also_ having access to the machine that produced the output, to determine the unique key.  Nevertheless, for some purposes such as software testing, it may be desirable to set the unique key to a known value. This can be done using the function `set_unique_key`:

```python
>>> import trinomial
>>> trinomial.set_unique_key('my secret unique key here')
```

**Do not do this in production code**. Setting the value in your code makes it much easier for someone to try to reverse the process of producing the output. The function `set_unique_key` is meant for testing and debugging.


## Known issues and limitations

Trinomial is intended as a simple package to replace meaningful textual information with meaningless identifiers, such that (a) it is impractically difficult to discover the original text given only such an identifier, and (b) correlations between occurrences of the original text are preserved. However, it is at best a pseudoanonymization tool. It is not intended for sensitive applications, or legal requirements such as the GDPR,  HIPAA, or similar situations.

The possibility of output collisions between two or more identical input values is low, but not zero. The calculation of collisions for a hash function is based on the number of bits _b_ in the hashed output value, according to the function 2<sup>b/2</sup>.  A hexadecimal character can encode 4 bits, which means a hexadecimal string of length _n_ is equal to _n_&times;4 bits. This means that the **Trinomial default length of 10 output characters gives a maximum of 2<sup>(4&times;10)/2</sup> = 1,048,576 possible unique values**. In the author's opinion, this is reasonable for a situation such as (e.g.) anonymizing email addresses in the logs of a program at a small educational institution, but may be too low for other situations. Users may want to increase the `length` parameter to `anon` accordingly.


## Getting help

If you find an issue, please submit it in [the GitHub issue tracker](https://github.com/caltechlibrary/trinomial/issues) for this repository.


## Contributing

We would be happy to receive your help and participation with enhancing Trinomial!  Please visit the [guidelines for contributing](CONTRIBUTING.md) for some tips on getting started.


## License

Software produced by the Caltech Library is Copyright (C) 2021, Caltech.  This software is freely distributed under a BSD/MIT type license.  Please see the [LICENSE](LICENSE) file for more information.


## Authors and history

Trinomial was designed and implemented by [Michael Hucka](https://github.com/mhucka).


## Acknowledgments

This work was funded by the California Institute of Technology Library.

The [vector artwork](https://thenounproject.com/term/anonymous/225644/) used as a starting point for the logo for this repository was created by [Rflor](https://thenounproject.com/rflor/) for the [Noun Project](https://thenounproject.com).  It is licensed under the Creative Commons [Attribution 3.0 Unported](https://creativecommons.org/licenses/by/3.0/deed.en) license.  The vector graphics was modified by Mike Hucka to change the color.

<div align="center">
  <br>
  <a href="https://www.caltech.edu">
    <img width="100" height="100" src="https://raw.githubusercontent.com/caltechlibrary/trinomial/main/.graphics/caltech-round.png">
  </a>
</div>

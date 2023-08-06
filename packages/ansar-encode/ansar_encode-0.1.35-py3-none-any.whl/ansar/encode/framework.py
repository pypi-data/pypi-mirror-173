# Author: Scott Woods <scott.suzuki@gmail.com>
# MIT License
#
# Copyright (c) 2017-2022 Scott Woods
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Classes and functions supporting the concept of a standard process.

Support for standard behaviour around the starting and stopping of a
process - command line arguments, configuration, exit values and standard
streams.
"""
__docformat__ = 'restructuredtext'

__all__ = [
    'program_name',
    'command_args',
]

import re

#
#
KEY_EQUALS_VALUE = '([a-zA-Z][-_a-zA-Z0-9]*)(=(.*))?'
LETTERS_ONLY = '[a-zA-Z0-9]+'

kev = re.compile(KEY_EQUALS_VALUE)
lo = re.compile(LETTERS_ONLY)

program_name = '<not-set>'

def command_args(argv):
    """Breakdown command-line arguments into name=value pairs, letter flags and words.

    :param argv: the arguments passed to a process
    :type path: list of string
    """
    global program_name
    program_name = argv[0]

    kv = {}
    flags = {}
    args = []
    for a in argv[1:]:
        if a.startswith('--'):
            t = a[2:]
            m = kev.match(t)
            if m:
                underscored = m.group(1).replace('-', '_')
                if m.group(2):
                    kv[underscored] = m.group(3)
                else:
                    kv[underscored] = 'true'
                continue
            raise ValueError('non-standard long-form argument "%s"' % (t,))
        elif a.startswith('-'):
            t = a[1:]
            m = lo.match(t)
            if m:
                for c in m.group():
                    flags[c] = len(args)
                continue
            raise ValueError('non-standard short-form argument "%s"' % (t,))
        else:
            args.append(a)
    # Return the separated bundles.
    return kv, flags, args

import sys

PY3 = sys.version_info[0] >= 3
PY2 = not PY3

if PY3:  # pragma: no cover

    string_types = str,
    text_type = str
    binary_type = bytes
    integer_types = int,

    def non_native_string(x):
        if isinstance(x, bytes):
            return x
        return bytes(x, 'unicode_escape')

    def make_binary(x):
        if isinstance(x, bytes):
            return x
        return x.encode('ascii')

else:  # pragma: no cover

    string_types = basestring,
    text_type = unicode
    binary_type = str
    integer_types = (int, long)

    def non_native_string(x):
        if isinstance(x, unicode):
            return x
        return unicode(x, 'unicode_escape')

    def make_binary(x):
        if isinstance(x, str):
            return x
        return x.encode('ascii')

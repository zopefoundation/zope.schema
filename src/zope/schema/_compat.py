import sys

PY3 = sys.version_info[0] >= 3

if PY3: #pragma NO COVER
    import builtins
    def b(s):
        return s.encode("latin-1")
    def u(s):
        return s
    string_types = str,
    text_type = str
    binary_type = bytes
    integer_types = int,
    non_native_string = bytes
else: #pragma NO COVER
    def b(s):
        return s
    def u(s):
        return unicode(s, "unicode_escape")
    string_types = basestring,
    text_type = unicode
    binary_type = str
    integer_types = (int, long)
    non_native_string = unicode

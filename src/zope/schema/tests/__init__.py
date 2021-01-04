#
# This file is necessary to make this directory a package.

import re

from zope.schema._compat import PY3
from zope.testing import renormalizing


def _make_transforms(patterns):
    return [(re.compile(pattern), repl) for pattern, repl in patterns]


if PY3:  # pragma: PY3
    py3_checker = renormalizing.RENormalizing(_make_transforms([
        (r"u'([^']*)'",
         r"'\1'"),
        (r"^b'([^']*)'",
         r"'\1'"),
        (r"([^'])b'([^']*)'",
         r"\1'\2'"),
        (r"<class 'bytes'>",
         r"<type 'str'>"),
        (r"<class 'str'>",
         r"<type 'unicode'>"),
        (r"zope.schema._bootstrapinterfaces.InvalidValue",
         r"InvalidValue"),
        (r"zope.schema.interfaces.InvalidId: '([^']*)'",
         r"InvalidId: \1"),
        (r"zope.schema.interfaces.InvalidId:",
         r"InvalidId:"),
        (r"zope.schema.interfaces.InvalidURI: '([^']*)'",
         r"InvalidURI: \1"),
        (r"zope.schema.interfaces.InvalidURI:",
         r"InvalidURI:"),
        (r"zope.schema.interfaces.InvalidDottedName: '([^']*)'",
         r"InvalidDottedName: \1"),
        (r"zope.schema.interfaces.InvalidDottedName:",
         r"InvalidDottedName:"),
        (r"zope.schema._bootstrapinterfaces.ConstraintNotSatisfied: '([^']*)'",
         r"ConstraintNotSatisfied: \1"),
        (r"zope.schema._bootstrapinterfaces.ConstraintNotSatisfied:",
         r"ConstraintNotSatisfied:"),
        (r"zope.schema._bootstrapinterfaces.WrongType:",
         r"WrongType:"),
    ]))
else:  # pragma: PY2
    py3_checker = renormalizing.RENormalizing(_make_transforms([
        (r"([^'])b'([^']*)'",
         r"\1'\2'"),
    ]))

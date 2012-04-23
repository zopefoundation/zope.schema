##############################################################################
#
# Copyright (c) 2012 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
import unittest


class BytesTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._field import Bytes
        return Bytes

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_fromUnicode_miss(self):
        from zope.schema._compat import u
        byt = self._makeOne()
        self.assertRaises(UnicodeEncodeError, byt.fromUnicode, u(chr(129)))

    def test_fromUnicode_hit(self):
        from zope.schema._compat import u
        from zope.schema._compat import b
        byt = self._makeOne()
        self.assertEqual(byt.fromUnicode(u('')), b(''))
        self.assertEqual(byt.fromUnicode(u('DEADBEEF')), b('DEADBEEF'))


class ASCIITests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._field import ASCII
        return ASCII

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test__validate_empty(self):
        asc = self._makeOne()
        asc._validate('') # no error

    def test__validate_non_empty_miss(self):
        from zope.schema.interfaces import InvalidValue
        asc = self._makeOne()
        self.assertRaises(InvalidValue, asc._validate, chr(129))

    def test__validate_non_empty_hit(self):
        asc = self._makeOne()
        for i in range(128):
            asc._validate(chr(i)) #doesn't raise


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(BytesTests),
        unittest.makeSuite(ASCIITests),
    ))


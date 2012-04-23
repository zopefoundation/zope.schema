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


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(BytesTests),
    ))


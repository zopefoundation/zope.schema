##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
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
"""Integer field tests
"""
import unittest

from zope.schema.tests.test_field import FieldTestBase


class IntTest(unittest.TestCase, FieldTestBase):
    """Test the Int Field."""

    def _getTargetClass(self):
        from zope.schema import Int
        return Int

    def testValidate(self):
        from zope.schema._compat import u
        field = self._makeOne(title=u('Int field'), description=u(''),
                                    readonly=False, required=False)
        field.validate(None)
        field.validate(10)
        field.validate(0)
        field.validate(-1)

    def testValidateRequired(self):
        from zope.schema._compat import u
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne(title=u('Int field'), description=u(''),
                                    readonly=False, required=True)
        field.validate(10)
        field.validate(0)
        field.validate(-1)

        self.assertRaises(RequiredMissing, field.validate, None)

    def testValidateMin(self):
        from zope.schema._compat import u
        from zope.schema.interfaces import TooSmall
        field = self._makeOne(title=u('Int field'), description=u(''),
                                    readonly=False, required=False, min=10)
        field.validate(None)
        field.validate(10)
        field.validate(20)

        self.assertRaises(TooSmall, field.validate, 9)
        self.assertRaises(TooSmall, field.validate, -10)

    def testValidateMax(self):
        from zope.schema._compat import u
        from zope.schema.interfaces import TooBig
        field = self._makeOne(title=u('Int field'), description=u(''),
                                    readonly=False, required=False, max=10)
        field.validate(None)
        field.validate(5)
        field.validate(9)
        field.validate(10)

        self.assertRaises(TooBig, field.validate, 11)
        self.assertRaises(TooBig, field.validate, 20)

    def testValidateMinAndMax(self):
        from zope.schema._compat import u
        from zope.schema.interfaces import TooBig
        from zope.schema.interfaces import TooSmall
        field = self._makeOne(title=u('Int field'), description=u(''),
                                    readonly=False, required=False,
                                    min=0, max=10)
        field.validate(None)
        field.validate(0)
        field.validate(5)
        field.validate(10)

        self.assertRaises(TooSmall, field.validate, -10)
        self.assertRaises(TooSmall, field.validate, -1)
        self.assertRaises(TooBig, field.validate, 11)
        self.assertRaises(TooBig, field.validate, 20)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(IntTest),
    ))

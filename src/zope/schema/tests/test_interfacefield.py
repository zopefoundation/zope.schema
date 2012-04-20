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
"""Interface field tests
"""
import unittest

from zope.schema.tests.test_field import FieldTestBase

class InterfaceTest(unittest.TestCase, FieldTestBase):
    """Test the Bool Field."""

    def _getTargetClass(self):
        from zope.schema import InterfaceField
        return InterfaceField

    def testValidate(self):
        from zope.schema._compat import u
        from zope.interface import Interface
        from zope.schema.interfaces import WrongType

        class DummyInterface(Interface):
            pass

        field = self._makeOne(title=u('Interface field'), description=u(''),
                     readonly=False, required=False)
        field.validate(DummyInterface)
        self.assertRaises(WrongType, field.validate, object())

    def testValidateRequired(self):
        from zope.schema._compat import u
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne(title=u('Interface field'), description=u(''),
                     readonly=False, required=True)
        self.assertRaises(RequiredMissing, field.validate, None)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(InterfaceTest),
    ))

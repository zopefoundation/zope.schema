##############################################################################
#
# Copyright (c) 2010 Zope Foundation and Contributors.
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
"""DottedName field tests
"""
import unittest

from zope.schema.tests.test_field import FieldTestBase


class DottedNameTest(unittest.TestCase, FieldTestBase):
    """Test the DottedName Field."""

    def _getTargetClass(self):
        from zope.schema import DottedName
        return DottedName

    def testValidate(self):
        from zope.schema.interfaces import InvalidDottedName
        field = self._makeOne(required=False)

        field.validate(None)
        field.validate('foo.bar')
        field.validate('foo.bar0')
        field.validate('foo0.bar')
        
        # We used to incorrectly allow ^:
        #  https://bugs.launchpad.net/zope.schema/+bug/191236
        self.assertRaises(InvalidDottedName, field.validate, 'foo.bar^foobar')
        self.assertRaises(InvalidDottedName, field.validate, 'foo^foobar.bar')
        # dotted names cannot start with digits
        self.assertRaises(InvalidDottedName, field.validate, 'foo.0bar')
        self.assertRaises(InvalidDottedName, field.validate, '0foo.bar')

    def testValidateRequired(self):
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne(required=True)
        
        field.validate('foo.bar')
        
        self.assertRaises(RequiredMissing, field.validate, None)

    def testFromUnicode(self):
        from zope.schema._compat import u
        field = self._makeOne()
        self.assertEqual(field.fromUnicode(u('foo')), 'foo')


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(DottedNameTest),
    ))

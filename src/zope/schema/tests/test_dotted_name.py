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
from unittest import main, makeSuite

from six import b, u
from zope.schema import DottedName
from zope.schema.tests.test_field import FieldTestBase
from zope.schema.interfaces import InvalidDottedName, RequiredMissing

class DottedNameTest(FieldTestBase):
    """Test the DottedName Field."""

    _Field_Factory = DottedName

    def testValidate(self):
        field = self._Field_Factory(required=False)

        field.validate(None)
        field.validate('foo.bar')
        field.validate('foo.bar0')
        field.validate('foo0.bar')
        
        # We used to incorrectly allow ^: https://bugs.launchpad.net/zope.schema/+bug/191236
        self.assertRaises(InvalidDottedName, field.validate, 'foo.bar^foobar')
        self.assertRaises(InvalidDottedName, field.validate, 'foo^foobar.bar')
        # dotted names cannot start with digits
        self.assertRaises(InvalidDottedName, field.validate, 'foo.0bar')
        self.assertRaises(InvalidDottedName, field.validate, '0foo.bar')

    def testValidateRequired(self):
        field = self._Field_Factory(required=True)
        
        field.validate('foo.bar')
        
        self.assertRaises(RequiredMissing, field.validate, None)

    def testFromUnicode(self):
        field = self._Field_Factory()
        self.assertEquals(field.fromUnicode(u('foo')), 'foo')


def test_suite():
    suite = makeSuite(DottedNameTest)
    return suite

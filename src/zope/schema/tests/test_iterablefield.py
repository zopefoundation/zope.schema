##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
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
"""Iterable field tests
"""
import unittest

from zope.schema.tests.test_field import FieldTestBase


class IterableTest(FieldTestBase):
    """Test the Iterable Field."""

    def _getTargetClass(self):
        from zope.schema import Iterable
        return Iterable

    def testValidate(self):
        try:
            from UserDict import UserDict
        except ImportError: #pragma NO COVER python3
            from collections import UserDict
            IterableUserDict =  UserDict
        else: #pragma NO COVER python2
            from UserDict import IterableUserDict
        from six import u
        from zope.schema.interfaces import NotAContainer
        from zope.schema.interfaces import NotAnIterator
        field = self._makeOne(title=u('test field'), description=u(''),
                              readonly=False, required=False)
        field.validate(None)
        field.validate('')
        field.validate('abc')
        field.validate([1, 2, 3])
        field.validate({'a': 1, 'b': 2})
        field.validate(IterableUserDict())

        self.assertRaises(NotAContainer, field.validate, 1)
        self.assertRaises(NotAContainer, field.validate, True)
        self.assertRaises(NotAnIterator, field.validate, UserDict)

    def testValidateRequired(self):
        from six import u
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne(title=u('test field'), description=u(''),
                              readonly=False, required=True)
        field.validate('')
        self.assertRaises(RequiredMissing, field.validate, None)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(IterableTest),
    ))


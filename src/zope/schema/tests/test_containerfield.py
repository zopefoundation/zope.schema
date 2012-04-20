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
"""Container field tests
"""
import unittest

from zope.schema.tests.test_field import FieldTestBase

class ContainerTest(unittest.TestCase, FieldTestBase):
    """Test the Container Field."""

    def _getTargetClass(self):
        from zope.schema import Container
        return Container

    def testValidate(self):
        try:
            from UserDict import UserDict
        except ImportError: #pragma NO COVER python3
            from collections import UserDict
        from zope.schema._compat import u
        from zope.schema.interfaces import NotAContainer
        field = self._makeOne(title=u('test field'), description=u(''),
                              readonly=False, required=False)
        field.validate(None)
        field.validate('')
        field.validate('abc')
        field.validate([1, 2, 3])
        field.validate({'a': 1, 'b': 2})
        field.validate(UserDict())

        self.assertRaises(NotAContainer, field.validate, 1)
        self.assertRaises(NotAContainer, field.validate, True)

    def testValidateRequired(self):
        from zope.schema._compat import u
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne(title=u('test field'), description=u(''),
                              readonly=False, required=True)
        field.validate('')
        self.assertRaises(RequiredMissing, field.validate, None)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(ContainerTest),
    ))

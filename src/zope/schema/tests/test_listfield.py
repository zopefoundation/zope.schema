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
"""List field tests
"""
import unittest

from zope.schema.tests.test_field import CollectionFieldTestBase


class ListTest(unittest.TestCase, CollectionFieldTestBase):
    """Test the List Field."""

    def _getTargetClass(self):
        from zope.schema import List
        return List

    def testValidate(self):
        from zope.schema._compat import u
        field = self._makeOne(title=u('List field'), description=u(''),
                     readonly=False, required=False)
        field.validate(None)
        field.validate([])
        field.validate([1, 2])
        field.validate([3,])

    def testValidateRequired(self):
        from zope.schema._compat import u
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne(title=u('List field'), description=u(''),
                     readonly=False, required=True)
        field.validate([])
        field.validate([1, 2])
        field.validate([3,])

        self.assertRaises(RequiredMissing, field.validate, None)

    def testValidateMinValues(self):
        from zope.schema._compat import u
        from zope.schema.interfaces import TooShort
        field = self._makeOne(title=u('List field'), description=u(''),
                     readonly=False, required=False, min_length=2)
        field.validate(None)
        field.validate([1, 2])
        field.validate([1, 2, 3])

        self.assertRaises(TooShort, field.validate, [])
        self.assertRaises(TooShort, field.validate, [1,])

    def testValidateMaxValues(self):
        from zope.schema._compat import u
        from zope.schema.interfaces import TooLong
        field = self._makeOne(title=u('List field'), description=u(''),
                     readonly=False, required=False, max_length=2)
        field.validate(None)
        field.validate([])
        field.validate([1, 2])

        self.assertRaises(TooLong, field.validate, [1, 2, 3, 4])
        self.assertRaises(TooLong, field.validate, [1, 2, 3])

    def testValidateMinValuesAndMaxValues(self):
        from zope.schema._compat import u
        from zope.schema.interfaces import TooLong
        from zope.schema.interfaces import TooShort
        field = self._makeOne(title=u('List field'), description=u(''),
                     readonly=False, required=False,
                     min_length=1, max_length=2)
        field.validate(None)
        field.validate([1, ])
        field.validate([1, 2])

        self.assertRaises(TooShort, field.validate, [])
        self.assertRaises(TooLong, field.validate, [1, 2, 3])

    def testValidateValueTypes(self):
        from zope.schema._compat import u
        from zope.schema import Int
        from zope.schema.interfaces import WrongContainedType
        field = self._makeOne(title=u('List field'), description=u(''),
                     readonly=False, required=False,
                     value_type=Int())
        field.validate(None)
        field.validate([5,])
        field.validate([2, 3])

        self.assertRaises(WrongContainedType, field.validate, ['',] )
        self.assertRaises(WrongContainedType, field.validate, [3.14159,] )

    def testCorrectValueType(self):
        # TODO: We should not allow for a None valeu type. 
        from zope.interface import implementer
        from zope.schema import Field
        from zope.schema.interfaces import IField
        self._makeOne(value_type=None)

        # do not allow arbitrary value types
        self.assertRaises(ValueError, self._makeOne, value_type=object())
        self.assertRaises(ValueError, self._makeOne, value_type=Field)

        # however, allow anything that implements IField
        self._makeOne(value_type=Field())
        @implementer(IField)
        class FakeField(object):
            pass
        self._makeOne(value_type=FakeField())

    def testUnique(self):
        from zope.schema._compat import u
        from zope.schema.interfaces import NotUnique
        field = self._makeOne(title=u('test field'), description=u(''),
                                    readonly=False, required=True, unique=True)
        field.validate([1, 2])
        self.assertRaises(NotUnique, field.validate, [1, 2, 1])
    
    def testImplements(self):
        from zope.schema.interfaces import ICollection
        from zope.schema.interfaces import IList
        from zope.schema.interfaces import ISequence
        field = self._makeOne()
        self.assertTrue(IList.providedBy(field))
        self.assertTrue(ISequence.providedBy(field))
        self.assertTrue(ICollection.providedBy(field))


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(ListTest),
    ))

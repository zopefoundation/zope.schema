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
"""Set field tests.
"""
import unittest

from zope.schema.tests.test_field import CollectionFieldTestBase


class SetTest(CollectionFieldTestBase):
    """Test the Tuple Field."""

    def _getTargetClass(self):
        from zope.schema import Set
        return Set

    def testValidate(self):
        from six import u
        from zope.schema.interfaces import WrongType
        field = self._makeOne(title=u('Set field'), description=u(''),
                    readonly=False, required=False)
        field.validate(None)
        field.validate(set())
        field.validate(set((1, 2)))
        field.validate(set((3,)))
        field.validate(set())
        field.validate(set((1, 2)))
        field.validate(set((3,)))

        self.assertRaises(WrongType, field.validate, [1, 2, 3])
        self.assertRaises(WrongType, field.validate, 'abc')
        self.assertRaises(WrongType, field.validate, 1)
        self.assertRaises(WrongType, field.validate, {})
        self.assertRaises(WrongType, field.validate, (1, 2, 3))
        self.assertRaises(WrongType, field.validate, frozenset((1, 2, 3)))

    def testValidateRequired(self):
        from six import u
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne(title=u('Set field'), description=u(''),
                    readonly=False, required=True)
        field.validate(set())
        field.validate(set((1, 2)))
        field.validate(set((3,)))
        field.validate(set())
        field.validate(set((1, 2)))
        field.validate(set((3,)))

        self.assertRaises(RequiredMissing, field.validate, None)

    def testValidateRequiredAltMissingValue(self):
        from zope.schema.interfaces import RequiredMissing
        missing = object()
        field = self._makeOne(required=True, missing_value=missing)
        field.validate(set())
        field.validate(set())

        self.assertRaises(RequiredMissing, field.validate, missing)

    def testValidateDefault(self):
        field = self._makeOne(required=True)
        field.default = None

    def testValidateDefaultAltMissingValue(self):
        missing = object()
        field = self._makeOne(required=True, missing_value=missing)
        field.default = missing

    def testValidateMinValues(self):
        from six import u
        from zope.schema.interfaces import TooShort
        field = self._makeOne(title=u('Set field'), description=u(''),
                    readonly=False, required=False, min_length=2)
        field.validate(None)
        field.validate(set((1, 2)))
        field.validate(set((1, 2, 3)))
        field.validate(set((1, 2)))
        field.validate(set((1, 2, 3)))

        self.assertRaises(TooShort, field.validate, set(()))
        self.assertRaises(TooShort, field.validate, set((3,)))
        self.assertRaises(TooShort, field.validate, set(()))
        self.assertRaises(TooShort, field.validate, set((3,)))

    def testValidateMaxValues(self):
        from six import u
        from zope.schema.interfaces import TooLong
        field = self._makeOne(title=u('Set field'), description=u(''),
                    readonly=False, required=False, max_length=2)
        field.validate(None)
        field.validate(set())
        field.validate(set((1, 2)))
        field.validate(set())
        field.validate(set((1, 2)))

        self.assertRaises(TooLong, field.validate, set((1, 2, 3, 4)))
        self.assertRaises(TooLong, field.validate, set((1, 2, 3)))
        self.assertRaises(TooLong, field.validate, set((1, 2, 3, 4)))
        self.assertRaises(TooLong, field.validate, set((1, 2, 3)))

    def testValidateMinValuesAndMaxValues(self):
        from six import u
        from zope.schema.interfaces import TooLong
        from zope.schema.interfaces import TooShort
        field = self._makeOne(title=u('Set field'), description=u(''),
                    readonly=False, required=False,
                    min_length=1, max_length=2)
        field.validate(None)
        field.validate(set((3,)))
        field.validate(set((1, 2)))
        field.validate(set((3,)))
        field.validate(set((1, 2)))

        self.assertRaises(TooShort, field.validate, set())
        self.assertRaises(TooLong, field.validate, set((1, 2, 3)))
        self.assertRaises(TooShort, field.validate, set())
        self.assertRaises(TooLong, field.validate, set((1, 2, 3)))

    def testValidateValueTypes(self):
        from six import u
        from zope.schema import Int
        from zope.schema.interfaces import WrongContainedType
        field = self._makeOne(title=u('Set field'), description=u(''),
                    readonly=False, required=False,
                    value_type=Int())
        field.validate(None)
        field.validate(set((5,)))
        field.validate(set((2, 3)))
        field.validate(set((5,)))
        field.validate(set((2, 3)))

        self.assertRaises(WrongContainedType, field.validate,
                          set(('',)))
        self.assertRaises(WrongContainedType, 
                          field.validate, set((3.14159,)))
        self.assertRaises(WrongContainedType, field.validate, set(('',)))
        self.assertRaises(WrongContainedType, 
                          field.validate, set((3.14159,)))

    def testCorrectValueType(self):
        from zope.interface import implementer
        from zope.schema import Field
        from zope.schema.interfaces import IField
        # TODO: We should not allow for a None value type. 
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
    
    def testNoUniqueArgument(self):
        self.assertRaises(TypeError, self._makeOne, unique=False)
        self.assertRaises(TypeError, self._makeOne, unique=True)
        self.assertTrue(self._makeOne().unique)
    
    def testImplements(self):
        from zope.schema.interfaces import IAbstractSet
        from zope.schema.interfaces import ICollection
        from zope.schema.interfaces import ISet
        from zope.schema.interfaces import IUnorderedCollection
        field = self._makeOne()
        self.assertTrue(ISet.providedBy(field))
        self.assertTrue(IUnorderedCollection.providedBy(field))
        self.assertTrue(IAbstractSet.providedBy(field))
        self.assertTrue(ICollection.providedBy(field))


class FrozenSetTest(CollectionFieldTestBase):
    """Test the Tuple Field."""

    def _getTargetClass(self):
        from zope.schema import FrozenSet
        return FrozenSet

    def testValidate(self):
        from six import u
        from zope.schema.interfaces import WrongType
        field = self._makeOne(title=u('Set field'), description=u(''),
                    readonly=False, required=False)
        field.validate(None)
        field.validate(frozenset())
        field.validate(frozenset((1, 2)))
        field.validate(frozenset((3,)))

        self.assertRaises(WrongType, field.validate, [1, 2, 3])
        self.assertRaises(WrongType, field.validate, 'abc')
        self.assertRaises(WrongType, field.validate, 1)
        self.assertRaises(WrongType, field.validate, {})
        self.assertRaises(WrongType, field.validate, (1, 2, 3))
        self.assertRaises(WrongType, field.validate, set((1, 2, 3)))
        self.assertRaises(WrongType, field.validate, set((1, 2, 3)))

    def testValidateRequired(self):
        from six import u
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne(title=u('Set field'), description=u(''),
                    readonly=False, required=True)
        field.validate(frozenset())
        field.validate(frozenset((1, 2)))
        field.validate(frozenset((3,)))

        self.assertRaises(RequiredMissing, field.validate, None)

    def testValidateRequiredAltMissingValue(self):
        from zope.schema.interfaces import RequiredMissing
        missing = object()
        field = self._makeOne(required=True, missing_value=missing)
        field.validate(frozenset())

        self.assertRaises(RequiredMissing, field.validate, missing)

    def testValidateDefault(self):
        field = self._makeOne(required=True)
        field.default = None

    def testValidateDefaultAltMissingValue(self):
        missing = object()
        field = self._makeOne(required=True, missing_value=missing)
        field.default = missing

    def testValidateMinValues(self):
        from six import u
        from zope.schema.interfaces import TooShort
        field = self._makeOne(title=u('FrozenSet field'), description=u(''),
                    readonly=False, required=False, min_length=2)
        field.validate(None)
        field.validate(frozenset((1, 2)))
        field.validate(frozenset((1, 2, 3)))

        self.assertRaises(TooShort, field.validate, frozenset(()))
        self.assertRaises(TooShort, field.validate, frozenset((3,)))

    def testValidateMaxValues(self):
        from six import u
        from zope.schema.interfaces import TooLong
        field = self._makeOne(title=u('FrozenSet field'), description=u(''),
                          readonly=False, required=False, max_length=2)
        field.validate(None)
        field.validate(frozenset())
        field.validate(frozenset((1, 2)))

        self.assertRaises(TooLong, field.validate, frozenset((1, 2, 3, 4)))
        self.assertRaises(TooLong, field.validate, frozenset((1, 2, 3)))

    def testValidateMinValuesAndMaxValues(self):
        from six import u
        from zope.schema.interfaces import TooLong
        from zope.schema.interfaces import TooShort
        field = self._makeOne(title=u('FrozenSet field'), description=u(''),
                          readonly=False, required=False,
                          min_length=1, max_length=2)
        field.validate(None)
        field.validate(frozenset((3,)))
        field.validate(frozenset((1, 2)))

        self.assertRaises(TooShort, field.validate, frozenset())
        self.assertRaises(TooLong, field.validate, frozenset((1, 2, 3)))

    def testValidateValueTypes(self):
        from six import u
        from zope.schema import Int
        from zope.schema.interfaces import WrongContainedType
        field = self._makeOne(title=u('FrozenSet field'), description=u(''),
                          readonly=False, required=False,
                          value_type=Int())
        field.validate(None)
        field.validate(frozenset((5,)))
        field.validate(frozenset((2, 3)))

        self.assertRaises(WrongContainedType, field.validate, frozenset(('',)))
        self.assertRaises(WrongContainedType, 
                          field.validate, frozenset((3.14159,)))

    def testCorrectValueType(self):
        from zope.interface import implementer
        from zope.schema import Field
        from zope.schema.interfaces import IField
        # TODO: We should not allow for a None value type. 
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
    
    def testNoUniqueArgument(self):
        self.assertRaises(TypeError, self._makeOne, unique=False)
        self.assertRaises(TypeError, self._makeOne, unique=True)
        self.assertTrue(self._makeOne().unique)
    
    def testImplements(self):
        from zope.schema.interfaces import IAbstractSet
        from zope.schema.interfaces import ICollection
        from zope.schema.interfaces import IFrozenSet
        from zope.schema.interfaces import IUnorderedCollection
        field = self._makeOne()
        self.assertTrue(IFrozenSet.providedBy(field))
        self.assertTrue(IAbstractSet.providedBy(field))
        self.assertTrue(IUnorderedCollection.providedBy(field))
        self.assertTrue(ICollection.providedBy(field))


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(SetTest),
        unittest.makeSuite(FrozenSetTest),
    ))

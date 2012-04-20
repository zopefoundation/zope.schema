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
"""Tuple field tests.
"""
import unittest

from zope.schema.tests.test_field import CollectionFieldTestBase


class TupleTest(unittest.TestCase, CollectionFieldTestBase):
    """Test the Tuple Field."""

    def _getTargetClass(self):
        from zope.schema import Tuple
        return Tuple

    def testValidate(self):
        from six import u
        from zope.schema.interfaces import WrongType
        field = self._makeOne(title=u('Tuple field'), description=u(''),
                      readonly=False, required=False)
        field.validate(None)
        field.validate(())
        field.validate((1, 2))
        field.validate((3,))

        self.assertRaises(WrongType, field.validate, [1, 2, 3])
        self.assertRaises(WrongType, field.validate, 'abc')
        self.assertRaises(WrongType, field.validate, 1)
        self.assertRaises(WrongType, field.validate, {})

    def testValidateRequired(self):
        from six import u
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne(title=u('Tuple field'), description=u(''),
                      readonly=False, required=True)
        field.validate(())
        field.validate((1, 2))
        field.validate((3,))

        self.assertRaises(RequiredMissing, field.validate, None)

    def testValidateMinValues(self):
        from six import u
        from zope.schema.interfaces import TooShort
        field = self._makeOne(title=u('Tuple field'), description=u(''),
                      readonly=False, required=False, min_length=2)
        field.validate(None)
        field.validate((1, 2))
        field.validate((1, 2, 3))

        self.assertRaises(TooShort, field.validate, ())
        self.assertRaises(TooShort, field.validate, (1,))

    def testValidateMaxValues(self):
        from six import u
        from zope.schema.interfaces import TooLong
        field = self._makeOne(title=u('Tuple field'), description=u(''),
                      readonly=False, required=False, max_length=2)
        field.validate(None)
        field.validate(())
        field.validate((1, 2))

        self.assertRaises(TooLong, field.validate, (1, 2, 3, 4))
        self.assertRaises(TooLong, field.validate, (1, 2, 3))

    def testValidateMinValuesAndMaxValues(self):
        from six import u
        from zope.schema.interfaces import TooLong
        from zope.schema.interfaces import TooShort
        field = self._makeOne(title=u('Tuple field'), description=u(''),
                      readonly=False, required=False,
                      min_length=1, max_length=2)
        field.validate(None)
        field.validate((1, ))
        field.validate((1, 2))

        self.assertRaises(TooShort, field.validate, ())
        self.assertRaises(TooLong, field.validate, (1, 2, 3))

    def testValidateValueTypes(self):
        from six import u
        from zope.schema import Int
        from zope.schema.interfaces import WrongContainedType
        field = self._makeOne(title=u('Tuple field'), description=u(''),
                      readonly=False, required=False,
                      value_type=Int())
        field.validate(None)
        field.validate((5,))
        field.validate((2, 3))

        self.assertRaises(WrongContainedType, field.validate, ('',) )
        self.assertRaises(WrongContainedType, field.validate, (3.14159,) )

    def testCorrectValueType(self):
        from zope.interface import implementer
        from zope.schema import Field
        from zope.schema.interfaces import IField
        # allow value_type of None (??? is this OK?)
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
        from six import u
        from zope.schema.interfaces import NotUnique
        field = self._makeOne(title=u('test field'), description=u(''),
                                    readonly=False, required=True, unique=True)
        field.validate((1, 2))
        self.assertRaises(NotUnique, field.validate, (1, 2, 1))
    
    def testImplements(self):
        from zope.schema.interfaces import ICollection
        from zope.schema.interfaces import ISequence
        from zope.schema.interfaces import ITuple
        field = self._makeOne()
        self.assertTrue(ITuple.providedBy(field))
        self.assertTrue(ISequence.providedBy(field))
        self.assertTrue(ICollection.providedBy(field))


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(TupleTest),
    ))

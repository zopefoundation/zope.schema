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

try:
    compare = cmp
except NameError:
    def compare(a, b):
        return -1 if a < b else (0 if a == b else 1)

class ValidationErrorTestsMixin(object):

    def _getTargetClass(self):
        raise NotImplementedError

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)


class ValidationErrorTests(ValidationErrorTestsMixin,
                           unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._bootstrapinterfaces import ValidationError
        return ValidationError

    def test_doc(self):
        class Derived(self._getTargetClass()):
            """DERIVED"""
        inst = Derived()
        self.assertEqual(inst.doc(), 'DERIVED')

    def test___cmp___no_args(self):
        ve = self._makeOne()
        self.assertEqual(compare(ve, object()), -1)
        self.assertEqual(compare(object(), ve), 1)

    def test___cmp___hit(self):
        left = self._makeOne('abc')
        right = self._makeOne('def')
        self.assertEqual(compare(left, right), -1)
        self.assertEqual(compare(left, left), 0)
        self.assertEqual(compare(right, left), 1)

    def test___eq___no_args(self):
        ve = self._makeOne()
        self.assertNotEqual(ve, object())
        self.assertNotEqual(object(), ve)

    def test___eq___w_args(self):
        left = self._makeOne('abc')
        right = self._makeOne('def')
        self.assertNotEqual(left, right)
        self.assertNotEqual(right, left)
        self.assertEqual(left, left)
        self.assertEqual(right, right)

    def test___str___no_value(self):
        ve = self._makeOne('argument')
        self.assertEqual(
            'Raised if the Validation process fails.\nargument', str(ve))

    def test___str___w_value(self):
        ve = self._makeOne('argument').with_field_and_value(None, 'value')
        self.assertEqual(
            'Raised if the Validation process fails.\nvalue', str(ve))


class TestRequiredMissing(ValidationErrorTestsMixin,
                          unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._bootstrapinterfaces import RequiredMissing
        return RequiredMissing

    def test___str__(self):
        error = self._makeOne()
        self.assertEqual('Required input is missing.', str(error))


class TestWrongType(ValidationErrorTestsMixin,
                    unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._bootstrapinterfaces import WrongType
        return WrongType

    def _makeOne(self, value, field):
        return super(TestWrongType, self)._makeOne(
            value, field._type, field.__name__).with_field_and_value(
                field, value)

    def test___str__(self):
        from zope.schema._bootstrapfields import Bool
        error = self._makeOne(0, Bool())
        self.assertEqual(
            'Object is of wrong type.\n0 is not an instance of bool',
            str(error))


class TestOutOfBounds(unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._bootstrapinterfaces import OutOfBounds
        return OutOfBounds

    def test_TOO_LARGE_repr(self):
        self.assertIn('TOO_LARGE', repr(self._getTargetClass().TOO_LARGE))

    def test_TOO_SMALL_repr(self):
        self.assertIn('TOO_SMALL', repr(self._getTargetClass().TOO_SMALL))


class TestTooBig(ValidationErrorTestsMixin,
                 unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._bootstrapinterfaces import TooBig
        return TooBig

    def test___str__(self):
        error = self._makeOne(2, 1)
        self.assertEqual('Value is too big\n2 > 1', str(error))


class TestTooSmall(ValidationErrorTestsMixin,
                   unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._bootstrapinterfaces import TooSmall
        return TooSmall

    def test___str__(self):
        error = self._makeOne(1, 2)
        self.assertEqual('Value is too small\n1 < 2', str(error))


class TestTooLong(ValidationErrorTestsMixin,
                  unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._bootstrapinterfaces import TooLong
        return TooLong

    def test___str__(self):
        error = self._makeOne('ab', 1)
        self.assertEqual("Value is too long\nlen('ab') > 1", str(error))


class TestTooShort(ValidationErrorTestsMixin,
                   unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._bootstrapinterfaces import TooShort
        return TooShort

    def test___str__(self):
        error = self._makeOne('a', 2)
        self.assertEqual("Value is too short\nlen('a') < 2", str(error))


class TestWrongContainedType(ValidationErrorTestsMixin,
                             unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._bootstrapinterfaces import WrongContainedType
        return WrongContainedType

    def test___str__(self):
        from zope.schema._bootstrapinterfaces import TooBig
        error = self._makeOne([TooBig(2, 1)])
        self.assertEqual(
            'Wrong contained type\nValue is too big\n2 > 1', str(error))


class TestSchemaNotCorrectlyImplemented(ValidationErrorTestsMixin,
                                        unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._bootstrapinterfaces import (
            SchemaNotCorrectlyImplemented)
        return SchemaNotCorrectlyImplemented

    def test___str___schema_errors(self):
        from zope.schema._bootstrapfields import Bool
        from zope.schema._bootstrapinterfaces import WrongType
        schema_errors = {
            u'flag': WrongType(
                0, bool, u'flag').with_field_and_value(Bool(), 0),
        }
        error = self._makeOne(
            list(schema_errors.values()), u'field', schema_errors, [])
        self.assertEqual(
            'An object failed schema or invariant validation.\n'
            'flag: Object is of wrong type.\n'
            '0 is not an instance of bool',
            str(error))

    def test___str___invariant_errors(self):
        from zope.schema._bootstrapinterfaces import TooBig
        invariant_errors = [TooBig(2, 1)]
        error = self._makeOne(invariant_errors, u'field', {}, invariant_errors)
        self.assertEqual(
            'An object failed schema or invariant validation.\n'
            'Value is too big\n'
            '2 > 1',
            str(error))

    def test___str___both_errors(self):
        from zope.schema._bootstrapfields import Bool
        from zope.schema._bootstrapinterfaces import (
            TooBig,
            WrongType,
        )
        schema_errors = {
            u'flag': WrongType(
                0, bool, u'flag').with_field_and_value(Bool(), 0),
        }
        invariant_errors = [TooBig(2, 1)]
        error = self._makeOne(
            list(schema_errors.values()) + invariant_errors, u'field',
            schema_errors, invariant_errors)
        self.assertEqual(
            'An object failed schema or invariant validation.\n'
            'flag: Object is of wrong type.\n'
            '0 is not an instance of bool\n'
            'Value is too big\n'
            '2 > 1',
            str(error))


class TestSchemaNotFullyImplemented(ValidationErrorTestsMixin,
                                    unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._bootstrapinterfaces import SchemaNotFullyImplemented
        return SchemaNotFullyImplemented

    def test___str__(self):
        error = self._makeOne(
            AttributeError("'str' object has no attribute 'count'"))
        self.assertEqual(
            "Schema not fully implemented\n"
            "'str' object has no attribute 'count'",
            str(error))


class TestSchemaNotProvided(ValidationErrorTestsMixin,
                            unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._bootstrapinterfaces import SchemaNotProvided
        return SchemaNotProvided

    def test___str__(self):
        from zope.interface import Interface

        class IFoo(Interface):
            pass

        error = self._makeOne(IFoo, 0)
        self.assertEqual(
            'Schema not provided\n0 does not provide IFoo', str(error))


class TestNotAnInterface(ValidationErrorTestsMixin,
                         unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._bootstrapinterfaces import NotAnInterface
        return NotAnInterface

    def test___str__(self):
        error = self._makeOne(0, u'field')
        self.assertEqual(
            'Object is not an interface.\n'
            '0 is not an instance of IInterface',
            str(error))

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
"""String field tests
"""
import unittest

from zope.schema.tests.test_field import FieldTestBase


class StrTestBase(FieldTestBase):
    """Test the Str Field."""

    def testValidate(self):
        from zope.schema._compat import u
        field = self._makeOne(title=u('Str field'), description=u(''),
                                    readonly=False, required=False)
        field.validate(None)
        field.validate(self._convert('foo'))
        field.validate(self._convert(''))

    def testValidateRequired(self):
        from zope.schema._compat import u
        from zope.schema.interfaces import RequiredMissing
        from zope.schema.interfaces import TooShort
        # Note that if we want to require non-empty strings,
        # we need to set the min-length to 1.

        field = self._makeOne(
            title=u('Str field'), description=u(''),
            readonly=False, required=True, min_length=1)
        field.validate(self._convert('foo'))

        self.assertRaises(RequiredMissing, field.validate, None)
        self.assertRaises(TooShort, field.validate, self._convert(''))

    def testValidateMinLength(self):
        from zope.schema._compat import u
        from zope.schema.interfaces import TooShort
        field = self._makeOne(
            title=u('Str field'), description=u(''),
            readonly=False, required=False, min_length=3)
        field.validate(None)
        field.validate(self._convert('333'))
        field.validate(self._convert('55555'))

        self.assertRaises(TooShort, field.validate, self._convert(''))
        self.assertRaises(TooShort, field.validate, self._convert('22'))
        self.assertRaises(TooShort, field.validate, self._convert('1'))

    def testValidateMaxLength(self):
        from zope.schema._compat import u
        from zope.schema.interfaces import TooLong
        field = self._makeOne(
            title=u('Str field'), description=u(''),
            readonly=False, required=False, max_length=5)
        field.validate(None)
        field.validate(self._convert(''))
        field.validate(self._convert('333'))
        field.validate(self._convert('55555'))

        self.assertRaises(TooLong, field.validate, self._convert('666666'))
        self.assertRaises(TooLong, field.validate, self._convert('999999999'))

    def testValidateMinLengthAndMaxLength(self):
        from zope.schema._compat import u
        from zope.schema.interfaces import TooLong
        from zope.schema.interfaces import TooShort
        field = self._makeOne(
            title=u('Str field'), description=u(''),
            readonly=False, required=False,
            min_length=3, max_length=5)

        field.validate(None)
        field.validate(self._convert('333'))
        field.validate(self._convert('4444'))
        field.validate(self._convert('55555'))

        self.assertRaises(TooShort, field.validate, self._convert('22'))
        self.assertRaises(TooShort, field.validate, self._convert('22'))
        self.assertRaises(TooLong, field.validate, self._convert('666666'))
        self.assertRaises(TooLong, field.validate, self._convert('999999999'))


class MultiLine(object):

    def test_newlines(self):
        from zope.schema._compat import u
        field = self._makeOne(title=u('Str field'))
        field.validate(self._convert('hello\nworld'))


class BytesTest(unittest.TestCase, StrTestBase, MultiLine):

    def _getTargetClass(self):
        from zope.schema import Bytes
        return Bytes

    def _convert(self, v):
        from zope.schema._compat import b
        return b(v)

    def testBadStringType(self):
        from zope.schema._compat import u
        from zope.schema.interfaces import ValidationError
        field = self._makeOne()
        self.assertRaises(ValidationError, field.validate, u('hello'))


class TextTest(unittest.TestCase, StrTestBase, MultiLine):

    def _getTargetClass(self):
        from zope.schema import Text
        return Text

    def _convert(self, v):
        from zope.schema._compat import u
        return u(v)

    def testBadStringType(self):
        from zope.schema._compat import b
        from zope.schema.interfaces import ValidationError
        field = self._makeOne()
        self.assertRaises(ValidationError, field.validate, b('hello'))

    def testSillyDefault(self):
        from zope.schema._compat import b
        from zope.schema.interfaces import ValidationError
        self.assertRaises(ValidationError, self._makeOne, default=b(""))

class SingleLine(object):

    def test_newlines(self):
        from zope.schema._compat import u
        from zope.schema.interfaces import ConstraintNotSatisfied
        field = self._makeOne(title=u('Str field'))
        self.assertRaises(ConstraintNotSatisfied,
                                    field.validate,
                                    self._convert('hello\nworld'))

class PasswordTest(SingleLine, TextTest):

    def _getTargetClass(self):
        from zope.schema import Password
        return Password

    def test_existingValue(self):
        from zope.schema._compat import u
        from zope.schema.interfaces import WrongType
        class Dummy(object):
            password = None
        dummy = Dummy()

        field = self._makeOne(title=u('Str field'), description=u(''),
                                    readonly=False, required=True,
                                    __name__='password')
        field = field.bind(dummy)

        # Using UNCHANGED_PASSWORD is not allowed if no password was set yet
        self.assertRaises(WrongType, field.validate, field.UNCHANGED_PASSWORD)

        dummy.password = 'asdf'
        field.validate(field.UNCHANGED_PASSWORD)

        # Using a normal value, the field gets updated
        field.set(dummy, u('test'))
        self.assertEqual(u('test'), dummy.password)

        # Using UNCHANGED_PASSWORD the field is not updated.
        field.set(dummy, field.UNCHANGED_PASSWORD)
        self.assertEqual(u('test'), dummy.password)


class BytesLineTest(SingleLine, BytesTest):

    def _getTargetClass(self):
        from zope.schema import BytesLine
        return BytesLine


class TextLineTest(SingleLine, TextTest):

    def _getTargetClass(self):
        from zope.schema import TextLine
        return TextLine


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(BytesTest),
        unittest.makeSuite(TextTest),
        unittest.makeSuite(BytesLineTest),
        unittest.makeSuite(TextLineTest),
        unittest.makeSuite(PasswordTest),
        ))


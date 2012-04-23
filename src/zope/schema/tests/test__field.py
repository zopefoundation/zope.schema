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


class BytesTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._field import Bytes
        return Bytes

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_fromUnicode_miss(self):
        from zope.schema._compat import u
        byt = self._makeOne()
        self.assertRaises(UnicodeEncodeError, byt.fromUnicode, u(chr(129)))

    def test_fromUnicode_hit(self):
        from zope.schema._compat import u
        from zope.schema._compat import b
        byt = self._makeOne()
        self.assertEqual(byt.fromUnicode(u('')), b(''))
        self.assertEqual(byt.fromUnicode(u('DEADBEEF')), b('DEADBEEF'))


class ASCIITests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._field import ASCII
        return ASCII

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test__validate_empty(self):
        asc = self._makeOne()
        asc._validate('') # no error

    def test__validate_non_empty_miss(self):
        from zope.schema.interfaces import InvalidValue
        asc = self._makeOne()
        self.assertRaises(InvalidValue, asc._validate, chr(129))

    def test__validate_non_empty_hit(self):
        asc = self._makeOne()
        for i in range(128):
            asc._validate(chr(i)) #doesn't raise


class BytesLineTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._field import BytesLine
        return BytesLine

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_constraint_miss(self):
        from zope.schema._compat import b
        bl = self._makeOne()
        self.assertEqual(bl.constraint(b('one line\nthen another')), False)

    def test_constraint_hit(self):
        from zope.schema._compat import b
        bl = self._makeOne()
        self.assertEqual(bl.constraint(b('')), True)
        self.assertEqual(bl.constraint(b('one line')), True)


class ASCIILineTests(BytesLineTests):

    def _getTargetClass(self):
        from zope.schema._field import ASCIILine
        return ASCIILine


class FloatTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._field import Float
        return Float

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_fromUnicode_miss(self):
        from zope.schema._compat import u
        flt = self._makeOne()
        self.assertRaises(ValueError, flt.fromUnicode, u(''))
        self.assertRaises(ValueError, flt.fromUnicode, u('abc'))
        self.assertRaises(ValueError, flt.fromUnicode, u('14.G'))

    def test_fromUnicode_hit(self):
        from zope.schema._compat import u
        flt = self._makeOne()
        self.assertEqual(flt.fromUnicode(u('0')), 0.0)
        self.assertEqual(flt.fromUnicode(u('1.23')), 1.23)
        self.assertEqual(flt.fromUnicode(u('1.23e6')), 1230000.0)


class DecimalTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._field import Decimal
        return Decimal

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_fromUnicode_miss(self):
        from zope.schema._compat import u
        flt = self._makeOne()
        self.assertRaises(ValueError, flt.fromUnicode, u(''))
        self.assertRaises(ValueError, flt.fromUnicode, u('abc'))
        self.assertRaises(ValueError, flt.fromUnicode, u('1.4G'))

    def test_fromUnicode_hit(self):
        from decimal import Decimal
        from zope.schema._compat import u
        flt = self._makeOne()
        self.assertEqual(flt.fromUnicode(u('0')), Decimal('0.0'))
        self.assertEqual(flt.fromUnicode(u('1.23')), Decimal('1.23'))
        self.assertEqual(flt.fromUnicode(u('12345.6')), Decimal('12345.6'))


class DateTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._field import Date
        return Date

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test__validate_miss(self):
        from datetime import datetime
        from zope.schema.interfaces import WrongType
        asc = self._makeOne()
        self.assertRaises(WrongType, asc._validate, datetime.now())


class ChoiceTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._field import Choice
        return Choice

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_wo_values_vocabulary_or_source(self):
        self.assertRaises(ValueError, self._makeOne)

    def test_ctor_invalid_vocabulary(self):
        self.assertRaises(ValueError, self._makeOne, vocabulary=object())

    def test_ctor_invalid_source(self):
        self.assertRaises(ValueError, self._makeOne, source=object())

    def test_ctor_both_vocabulary_and_source(self):
        self.assertRaises(ValueError,
                          self._makeOne, vocabulary='voc.name', source=object())

    def test_ctor_both_vocabulary_and_values(self):
        self.assertRaises(ValueError,
                          self._makeOne, vocabulary='voc.name', values=[1, 2])

    def test_ctor_w_values(self):
        from zope.schema.vocabulary import SimpleVocabulary
        choose = self._makeOne(values=[1, 2])
        self.assertTrue(isinstance(choose.vocabulary, SimpleVocabulary))
        self.assertEqual(sorted(choose.vocabulary.by_value.keys()), [1, 2])

    def test_ctor_w_named_vocabulary(self):
        choose = self._makeOne(vocabulary='voc.name')
        self.assertEqual(choose.vocabularyName, 'voc.name')

    def test_fromUnicode_miss(self):
        from zope.schema.interfaces import ConstraintNotSatisfied
        from zope.schema._compat import u
        flt = self._makeOne(values=(u('foo'), u('bar'), u('baz')))
        self.assertRaises(ConstraintNotSatisfied, flt.fromUnicode, u(''))
        self.assertRaises(ConstraintNotSatisfied, flt.fromUnicode, u('abc'))
        self.assertRaises(ConstraintNotSatisfied, flt.fromUnicode, u('1.4G'))

    def test_fromUnicode_hit(self):
        from zope.schema._compat import u
        flt = self._makeOne(values=(u('foo'), u('bar'), u('baz')))
        self.assertEqual(flt.fromUnicode(u('foo')), u('foo'))
        self.assertEqual(flt.fromUnicode(u('bar')), u('bar'))
        self.assertEqual(flt.fromUnicode(u('baz')), u('baz'))


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(BytesTests),
        unittest.makeSuite(ASCIITests),
        unittest.makeSuite(BytesLineTests),
        unittest.makeSuite(ASCIILineTests),
        unittest.makeSuite(FloatTests),
        unittest.makeSuite(DecimalTests),
        unittest.makeSuite(DateTests),
        unittest.makeSuite(ChoiceTests),
    ))


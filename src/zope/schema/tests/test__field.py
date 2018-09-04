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
import datetime
import decimal
import doctest
import unittest

from zope.schema.tests.test__bootstrapfields import OrderableMissingValueMixin
from zope.schema.tests.test__bootstrapfields import EqualityTestsMixin


# pylint:disable=protected-access
# pylint:disable=too-many-lines
# pylint:disable=inherit-non-class
# pylint:disable=no-member
# pylint:disable=blacklisted-name

class BytesTests(EqualityTestsMixin, unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._field import Bytes
        return Bytes

    def _getTargetInterface(self):
        from zope.schema.interfaces import IBytes
        return IBytes

    def test_validate_wrong_types(self):
        from zope.schema.interfaces import WrongType

        field = self._makeOne()
        self.assertRaises(WrongType, field.validate, u'')
        self.assertRaises(WrongType, field.validate, 1)
        self.assertRaises(WrongType, field.validate, 1.0)
        self.assertRaises(WrongType, field.validate, ())
        self.assertRaises(WrongType, field.validate, [])
        self.assertRaises(WrongType, field.validate, {})
        self.assertRaises(WrongType, field.validate, set())
        self.assertRaises(WrongType, field.validate, frozenset())
        self.assertRaises(WrongType, field.validate, object())

    def test_validate_w_invalid_default(self):

        from zope.schema.interfaces import ValidationError
        self.assertRaises(ValidationError, self._makeOne, default=u'')

    def test_validate_not_required(self):

        field = self._makeOne(required=False)
        field.validate(b'')
        field.validate(b'abc')
        field.validate(b'abc\ndef')
        field.validate(None)

    def test_validate_required(self):
        from zope.schema.interfaces import RequiredMissing

        field = self._makeOne()
        field.validate(b'')
        field.validate(b'abc')
        field.validate(b'abc\ndef')
        self.assertRaises(RequiredMissing, field.validate, None)

    def test_fromUnicode_miss(self):
        byt = self._makeOne()
        self.assertRaises(UnicodeEncodeError, byt.fromUnicode, u'\x81')

    def test_fromUnicode_hit(self):

        byt = self._makeOne()
        self.assertEqual(byt.fromUnicode(u''), b'')
        self.assertEqual(byt.fromUnicode(u'DEADBEEF'), b'DEADBEEF')


class ASCIITests(EqualityTestsMixin,
                 unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._field import ASCII
        return ASCII

    def _getTargetInterface(self):
        from zope.schema.interfaces import IASCII
        return IASCII

    def test_validate_wrong_types(self):
        from zope.schema.interfaces import WrongType
        from zope.schema._compat import non_native_string
        field = self._makeOne()
        self.assertRaises(WrongType, field.validate, non_native_string(''))
        self.assertRaises(WrongType, field.validate, 1)
        self.assertRaises(WrongType, field.validate, 1.0)
        self.assertRaises(WrongType, field.validate, ())
        self.assertRaises(WrongType, field.validate, [])
        self.assertRaises(WrongType, field.validate, {})
        self.assertRaises(WrongType, field.validate, set())
        self.assertRaises(WrongType, field.validate, frozenset())
        self.assertRaises(WrongType, field.validate, object())

    def test__validate_empty(self):
        asc = self._makeOne()
        asc._validate('')  # no error

    def test__validate_non_empty_miss(self):
        from zope.schema.interfaces import InvalidValue
        asc = self._makeOne()
        with self.assertRaises(InvalidValue) as exc:
            asc._validate(chr(129))

        invalid = exc.exception
        self.assertIs(invalid.field, asc)
        self.assertEqual(invalid.value, chr(129))

    def test__validate_non_empty_hit(self):
        asc = self._makeOne()
        for i in range(128):
            asc._validate(chr(i))  # doesn't raise


class BytesLineTests(EqualityTestsMixin,
                     unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._field import BytesLine
        return BytesLine

    def _getTargetInterface(self):
        from zope.schema.interfaces import IBytesLine
        return IBytesLine

    def test_validate_wrong_types(self):
        from zope.schema.interfaces import WrongType

        field = self._makeOne()
        self.assertRaises(WrongType, field.validate, u'')
        self.assertRaises(WrongType, field.validate, 1)
        self.assertRaises(WrongType, field.validate, 1.0)
        self.assertRaises(WrongType, field.validate, ())
        self.assertRaises(WrongType, field.validate, [])
        self.assertRaises(WrongType, field.validate, {})
        self.assertRaises(WrongType, field.validate, set())
        self.assertRaises(WrongType, field.validate, frozenset())
        self.assertRaises(WrongType, field.validate, object())

    def test_validate_not_required(self):

        field = self._makeOne(required=False)
        field.validate(None)
        field.validate(b'')
        field.validate(b'abc')
        field.validate(b'\xab\xde')

    def test_validate_required(self):
        from zope.schema.interfaces import RequiredMissing

        field = self._makeOne()
        field.validate(b'')
        field.validate(b'abc')
        field.validate(b'\xab\xde')
        self.assertRaises(RequiredMissing, field.validate, None)

    def test_constraint(self):

        field = self._makeOne()
        self.assertEqual(field.constraint(b''), True)
        self.assertEqual(field.constraint(b'abc'), True)
        self.assertEqual(field.constraint(b'abc'), True)
        self.assertEqual(field.constraint(b'\xab\xde'), True)
        self.assertEqual(field.constraint(b'abc\ndef'), False)


class ASCIILineTests(EqualityTestsMixin,
                     unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._field import ASCIILine
        return ASCIILine

    def _getTargetInterface(self):
        from zope.schema.interfaces import IASCIILine
        return IASCIILine

    def test_validate_wrong_types(self):
        from zope.schema.interfaces import WrongType
        from zope.schema._compat import non_native_string
        field = self._makeOne()
        self.assertRaises(WrongType, field.validate, non_native_string(''))
        self.assertRaises(WrongType, field.validate, 1)
        self.assertRaises(WrongType, field.validate, 1.0)
        self.assertRaises(WrongType, field.validate, ())
        self.assertRaises(WrongType, field.validate, [])
        self.assertRaises(WrongType, field.validate, {})
        self.assertRaises(WrongType, field.validate, set())
        self.assertRaises(WrongType, field.validate, frozenset())
        self.assertRaises(WrongType, field.validate, object())

    def test_validate_not_required(self):
        from zope.schema.interfaces import InvalidValue
        field = self._makeOne(required=False)
        field.validate(None)
        field.validate('')
        field.validate('abc')
        self.assertRaises(InvalidValue, field.validate, '\xab\xde')

    def test_validate_required(self):
        from zope.schema.interfaces import InvalidValue
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne()
        field.validate('')
        field.validate('abc')
        self.assertRaises(InvalidValue, field.validate, '\xab\xde')
        self.assertRaises(RequiredMissing, field.validate, None)

    def test_constraint(self):
        field = self._makeOne()
        self.assertEqual(field.constraint(''), True)
        self.assertEqual(field.constraint('abc'), True)
        self.assertEqual(field.constraint('abc'), True)
        # Non-ASCII byltes get checked in '_validate'.
        self.assertEqual(field.constraint('\xab\xde'), True)
        self.assertEqual(field.constraint('abc\ndef'), False)


class FloatTests(OrderableMissingValueMixin, EqualityTestsMixin,
                 unittest.TestCase):

    mvm_missing_value = -1.0
    mvm_default = 0.0

    def _getTargetClass(self):
        from zope.schema._field import Float
        return Float

    def _getTargetInterface(self):
        from zope.schema.interfaces import IFloat
        return IFloat

    def test_validate_not_required(self):
        field = self._makeOne(required=False)
        field.validate(None)
        field.validate(10.0)
        field.validate(0.93)
        field.validate(1000.0003)

    def test_validate_required(self):
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne()
        field.validate(10.0)
        field.validate(0.93)
        field.validate(1000.0003)
        self.assertRaises(RequiredMissing, field.validate, None)

    def test_validate_min(self):
        from zope.schema.interfaces import TooSmall
        field = self._makeOne(min=10.5)
        field.validate(10.6)
        field.validate(20.2)
        self.assertRaises(TooSmall, field.validate, -9.0)
        self.assertRaises(TooSmall, field.validate, 10.4)

    def test_validate_max(self):
        from zope.schema.interfaces import TooBig
        field = self._makeOne(max=10.5)
        field.validate(5.3)
        field.validate(-9.1)
        self.assertRaises(TooBig, field.validate, 10.51)
        self.assertRaises(TooBig, field.validate, 20.7)

    def test_validate_min_and_max(self):
        from zope.schema.interfaces import TooBig
        from zope.schema.interfaces import TooSmall
        field = self._makeOne(min=-0.6, max=10.1)
        field.validate(0.0)
        field.validate(-0.03)
        field.validate(10.0001)
        self.assertRaises(TooSmall, field.validate, -10.0)
        self.assertRaises(TooSmall, field.validate, -1.6)
        self.assertRaises(TooBig, field.validate, 11.45)
        self.assertRaises(TooBig, field.validate, 20.02)

    def test_fromUnicode_miss(self):

        flt = self._makeOne()
        self.assertRaises(ValueError, flt.fromUnicode, u'')
        self.assertRaises(ValueError, flt.fromUnicode, u'abc')
        self.assertRaises(ValueError, flt.fromUnicode, u'14.G')

    def test_fromUnicode_hit(self):

        flt = self._makeOne()
        self.assertEqual(flt.fromUnicode(u'0'), 0.0)
        self.assertEqual(flt.fromUnicode(u'1.23'), 1.23)
        self.assertEqual(flt.fromUnicode(u'1.23e6'), 1230000.0)


class DecimalTests(OrderableMissingValueMixin, EqualityTestsMixin,
                   unittest.TestCase):

    mvm_missing_value = decimal.Decimal("-1")
    mvm_default = decimal.Decimal("0")

    def _getTargetClass(self):
        from zope.schema._field import Decimal
        return Decimal

    def _getTargetInterface(self):
        from zope.schema.interfaces import IDecimal
        return IDecimal

    def test_validate_not_required(self):
        field = self._makeOne(required=False)
        field.validate(decimal.Decimal("10.0"))
        field.validate(decimal.Decimal("0.93"))
        field.validate(decimal.Decimal("1000.0003"))
        field.validate(None)

    def test_validate_required(self):
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne()
        field.validate(decimal.Decimal("10.0"))
        field.validate(decimal.Decimal("0.93"))
        field.validate(decimal.Decimal("1000.0003"))
        self.assertRaises(RequiredMissing, field.validate, None)

    def test_validate_min(self):
        from zope.schema.interfaces import TooSmall
        field = self._makeOne(min=decimal.Decimal("10.5"))
        field.validate(decimal.Decimal("10.6"))
        field.validate(decimal.Decimal("20.2"))
        self.assertRaises(TooSmall, field.validate, decimal.Decimal("-9.0"))
        self.assertRaises(TooSmall, field.validate, decimal.Decimal("10.4"))

    def test_validate_max(self):
        from zope.schema.interfaces import TooBig
        field = self._makeOne(max=decimal.Decimal("10.5"))
        field.validate(decimal.Decimal("5.3"))
        field.validate(decimal.Decimal("-9.1"))
        self.assertRaises(TooBig, field.validate, decimal.Decimal("10.51"))
        self.assertRaises(TooBig, field.validate, decimal.Decimal("20.7"))

    def test_validate_min_and_max(self):
        from zope.schema.interfaces import TooBig
        from zope.schema.interfaces import TooSmall
        field = self._makeOne(min=decimal.Decimal("-0.6"),
                              max=decimal.Decimal("10.1"))
        field.validate(decimal.Decimal("0.0"))
        field.validate(decimal.Decimal("-0.03"))
        field.validate(decimal.Decimal("10.0001"))
        self.assertRaises(TooSmall, field.validate, decimal.Decimal("-10.0"))
        with self.assertRaises(TooSmall) as exc:
            field.validate(decimal.Decimal("-1.6"))

        too_small = exc.exception
        self.assertIs(too_small.field, field)
        self.assertEqual(too_small.value, decimal.Decimal("-1.6"))

        self.assertRaises(TooBig, field.validate, decimal.Decimal("11.45"))
        with self.assertRaises(TooBig) as exc:
            field.validate(decimal.Decimal("20.02"))

        too_big = exc.exception
        self.assertIs(too_big.field, field)
        self.assertEqual(too_big.value, decimal.Decimal("20.02"))

    def test_fromUnicode_miss(self):
        from zope.schema.interfaces import ValidationError
        flt = self._makeOne()
        self.assertRaises(ValueError, flt.fromUnicode, u'')
        self.assertRaises(ValueError, flt.fromUnicode, u'abc')
        with self.assertRaises(ValueError) as exc:
            flt.fromUnicode(u'1.4G')

        value_error = exc.exception
        self.assertIs(value_error.field, flt)
        self.assertEqual(value_error.value, u'1.4G')
        self.assertIsInstance(value_error, ValidationError)

    def test_fromUnicode_hit(self):
        from decimal import Decimal

        flt = self._makeOne()
        self.assertEqual(flt.fromUnicode(u'0'), Decimal('0.0'))
        self.assertEqual(flt.fromUnicode(u'1.23'), Decimal('1.23'))
        self.assertEqual(flt.fromUnicode(u'12345.6'), Decimal('12345.6'))


class DatetimeTests(OrderableMissingValueMixin, EqualityTestsMixin,
                    unittest.TestCase):

    mvm_missing_value = datetime.datetime.now()
    mvm_default = datetime.datetime.now()

    def _getTargetClass(self):
        from zope.schema._field import Datetime
        return Datetime

    def _getTargetInterface(self):
        from zope.schema.interfaces import IDatetime
        return IDatetime

    def test_validate_wrong_types(self):
        from datetime import date
        from zope.schema.interfaces import WrongType


        field = self._makeOne()
        self.assertRaises(WrongType, field.validate, u'')
        self.assertRaises(WrongType, field.validate, u'')
        self.assertRaises(WrongType, field.validate, 1)
        self.assertRaises(WrongType, field.validate, 1.0)
        self.assertRaises(WrongType, field.validate, ())
        self.assertRaises(WrongType, field.validate, [])
        self.assertRaises(WrongType, field.validate, {})
        self.assertRaises(WrongType, field.validate, set())
        self.assertRaises(WrongType, field.validate, frozenset())
        self.assertRaises(WrongType, field.validate, object())
        self.assertRaises(WrongType, field.validate, date.today())

    def test_validate_not_required(self):
        field = self._makeOne(required=False)
        field.validate(None)  # doesn't raise
        field.validate(datetime.datetime.now())  # doesn't raise

    def test_validate_required(self):
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne(required=True)
        self.assertRaises(RequiredMissing, field.validate, None)

    def test_validate_w_min(self):
        from zope.schema.interfaces import TooSmall
        d1 = datetime.datetime(2000, 10, 1)
        d2 = datetime.datetime(2000, 10, 2)
        field = self._makeOne(min=d1)
        field.validate(d1)  # doesn't raise
        field.validate(d2)  # doesn't raise
        self.assertRaises(TooSmall, field.validate, datetime.datetime(2000, 9, 30))

    def test_validate_w_max(self):
        from zope.schema.interfaces import TooBig
        d1 = datetime.datetime(2000, 10, 1)
        d2 = datetime.datetime(2000, 10, 2)
        d3 = datetime.datetime(2000, 10, 3)
        field = self._makeOne(max=d2)
        field.validate(d1)  # doesn't raise
        field.validate(d2)  # doesn't raise
        self.assertRaises(TooBig, field.validate, d3)

    def test_validate_w_min_and_max(self):
        from zope.schema.interfaces import TooBig
        from zope.schema.interfaces import TooSmall
        d1 = datetime.datetime(2000, 10, 1)
        d2 = datetime.datetime(2000, 10, 2)
        d3 = datetime.datetime(2000, 10, 3)
        d4 = datetime.datetime(2000, 10, 4)
        d5 = datetime.datetime(2000, 10, 5)
        field = self._makeOne(min=d2, max=d4)
        field.validate(d2)  # doesn't raise
        field.validate(d3)  # doesn't raise
        field.validate(d4)  # doesn't raise
        self.assertRaises(TooSmall, field.validate, d1)
        self.assertRaises(TooBig, field.validate, d5)


class DateTests(OrderableMissingValueMixin, EqualityTestsMixin,
                unittest.TestCase):

    mvm_missing_value = datetime.date.today()
    mvm_default = datetime.date.today()

    def _getTargetClass(self):
        from zope.schema._field import Date
        return Date

    def _getTargetInterface(self):
        from zope.schema.interfaces import IDate
        return IDate

    def test_validate_wrong_types(self):
        from zope.schema.interfaces import WrongType

        field = self._makeOne()
        self.assertRaises(WrongType, field.validate, u'')
        self.assertRaises(WrongType, field.validate, u'')
        self.assertRaises(WrongType, field.validate, 1)
        self.assertRaises(WrongType, field.validate, 1.0)
        self.assertRaises(WrongType, field.validate, ())
        self.assertRaises(WrongType, field.validate, [])
        self.assertRaises(WrongType, field.validate, {})
        self.assertRaises(WrongType, field.validate, set())
        self.assertRaises(WrongType, field.validate, frozenset())
        self.assertRaises(WrongType, field.validate, object())
        now = datetime.datetime.now()
        with self.assertRaises(WrongType) as exc:
            field.validate(now)

        wrong_type = exc.exception
        self.assertIs(wrong_type.field, field)
        self.assertIs(wrong_type.value, now)

    def test_validate_not_required(self):
        from datetime import date
        field = self._makeOne(required=False)
        field.validate(None)
        field.validate(date.today())

    def test_validate_required(self):
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne()
        field.validate(datetime.datetime.now().date())
        self.assertRaises(RequiredMissing, field.validate, None)

    def test_validate_w_min(self):
        from datetime import date
        from zope.schema.interfaces import TooSmall
        d1 = date(2000, 10, 1)
        d2 = date(2000, 10, 2)
        field = self._makeOne(min=d1)
        field.validate(d1)
        field.validate(d2)
        field.validate(datetime.datetime.now().date())
        self.assertRaises(TooSmall, field.validate, date(2000, 9, 30))

    def test_validate_w_max(self):
        from datetime import date
        from zope.schema.interfaces import TooBig
        d1 = date(2000, 10, 1)
        d2 = date(2000, 10, 2)
        d3 = date(2000, 10, 3)
        field = self._makeOne(max=d2)
        field.validate(d1)
        field.validate(d2)
        self.assertRaises(TooBig, field.validate, d3)

    def test_validate_w_min_and_max(self):
        from datetime import date
        from zope.schema.interfaces import TooBig
        from zope.schema.interfaces import TooSmall
        d1 = date(2000, 10, 1)
        d2 = date(2000, 10, 2)
        d3 = date(2000, 10, 3)
        d4 = date(2000, 10, 4)
        d5 = date(2000, 10, 5)
        field = self._makeOne(min=d2, max=d4)
        field.validate(d2)
        field.validate(d3)
        field.validate(d4)
        self.assertRaises(TooSmall, field.validate, d1)
        self.assertRaises(TooBig, field.validate, d5)


class TimedeltaTests(OrderableMissingValueMixin, EqualityTestsMixin,
                     unittest.TestCase):

    mvm_missing_value = datetime.timedelta(minutes=15)
    mvm_default = datetime.timedelta(minutes=12)

    def _getTargetClass(self):
        from zope.schema._field import Timedelta
        return Timedelta

    def _getTargetInterface(self):
        from zope.schema.interfaces import ITimedelta
        return ITimedelta

    def test_validate_not_required(self):
        from datetime import timedelta
        field = self._makeOne(required=False)
        field.validate(None)
        field.validate(timedelta(minutes=15))

    def test_validate_required(self):
        from datetime import timedelta
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne()
        field.validate(timedelta(minutes=15))
        self.assertRaises(RequiredMissing, field.validate, None)

    def test_validate_min(self):
        from datetime import timedelta
        from zope.schema.interfaces import TooSmall
        t1 = timedelta(hours=2)
        t2 = timedelta(hours=3)
        field = self._makeOne(min=t1)
        field.validate(t1)
        field.validate(t2)
        self.assertRaises(TooSmall, field.validate, timedelta(hours=1))

    def test_validate_max(self):
        from datetime import timedelta
        from zope.schema.interfaces import TooBig
        t1 = timedelta(minutes=1)
        t2 = timedelta(minutes=2)
        t3 = timedelta(minutes=3)
        field = self._makeOne(max=t2)
        field.validate(t1)
        field.validate(t2)
        self.assertRaises(TooBig, field.validate, t3)

    def test_validate_min_and_max(self):
        from datetime import timedelta
        from zope.schema.interfaces import TooBig
        from zope.schema.interfaces import TooSmall
        t1 = timedelta(days=1)
        t2 = timedelta(days=2)
        t3 = timedelta(days=3)
        t4 = timedelta(days=4)
        t5 = timedelta(days=5)
        field = self._makeOne(min=t2, max=t4)
        field.validate(t2)
        field.validate(t3)
        field.validate(t4)
        self.assertRaises(TooSmall, field.validate, t1)
        self.assertRaises(TooBig, field.validate, t5)


class TimeTests(OrderableMissingValueMixin, EqualityTestsMixin,
                unittest.TestCase):

    mvm_missing_value = datetime.time(12, 15, 37)
    mvm_default = datetime.time(12, 25, 42)

    def _getTargetClass(self):
        from zope.schema._field import Time
        return Time

    def _getTargetInterface(self):
        from zope.schema.interfaces import ITime
        return ITime

    def test_validate_not_required(self):
        from datetime import time
        field = self._makeOne(required=False)
        field.validate(None)
        field.validate(time(12, 15, 37))

    def test_validate_required(self):
        from datetime import time
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne()
        field.validate(time(12, 15, 37))
        self.assertRaises(RequiredMissing, field.validate, None)

    def test_validate_min(self):
        from datetime import time
        from zope.schema.interfaces import TooSmall
        t1 = time(12, 15, 37)
        t2 = time(12, 25, 18)
        t3 = time(12, 42, 43)
        field = self._makeOne(min=t2)
        field.validate(t2)
        field.validate(t3)
        self.assertRaises(TooSmall, field.validate, t1)

    def test_validate_max(self):
        from datetime import time
        from zope.schema.interfaces import TooBig
        t1 = time(12, 15, 37)
        t2 = time(12, 25, 18)
        t3 = time(12, 42, 43)
        field = self._makeOne(max=t2)
        field.validate(t1)
        field.validate(t2)
        self.assertRaises(TooBig, field.validate, t3)

    def test_validate_min_and_max(self):
        from datetime import time
        from zope.schema.interfaces import TooBig
        from zope.schema.interfaces import TooSmall
        t1 = time(12, 15, 37)
        t2 = time(12, 25, 18)
        t3 = time(12, 42, 43)
        t4 = time(13, 7, 12)
        t5 = time(14, 22, 9)
        field = self._makeOne(min=t2, max=t4)
        field.validate(t2)
        field.validate(t3)
        field.validate(t4)
        self.assertRaises(TooSmall, field.validate, t1)
        self.assertRaises(TooBig, field.validate, t5)


class ChoiceTests(EqualityTestsMixin,
                  unittest.TestCase):

    def setUp(self):
        from zope.schema.vocabulary import _clear
        _clear()

    def tearDown(self):
        from zope.schema.vocabulary import _clear
        _clear()

    def _getTargetClass(self):
        from zope.schema._field import Choice
        return Choice

    def _makeOneFromClass(self, cls, *args, **kwargs):
        if (not args
            and 'vocabulary' not in kwargs
            and 'values' not in kwargs
            and 'source' not in kwargs):
            from zope.schema.vocabulary import SimpleVocabulary
            kwargs['vocabulary'] = SimpleVocabulary.fromValues([1, 2, 3])
        return super(ChoiceTests, self)._makeOneFromClass(cls, *args, **kwargs)

    def _getTargetInterface(self):
        from zope.schema.interfaces import IChoice
        return IChoice


    def test_ctor_wo_values_vocabulary_or_source(self):
        self.assertRaises(ValueError, self._getTargetClass())

    def test_ctor_invalid_vocabulary(self):
        self.assertRaises(ValueError, self._getTargetClass(), vocabulary=object())

    def test_ctor_invalid_source(self):
        self.assertRaises(ValueError, self._getTargetClass(), source=object())

    def test_ctor_both_vocabulary_and_source(self):
        self.assertRaises(
            ValueError,
            self._makeOne, vocabulary='voc.name', source=object()
        )

    def test_ctor_both_vocabulary_and_values(self):
        self.assertRaises(ValueError,
                          self._makeOne, vocabulary='voc.name', values=[1, 2])

    def test_ctor_w_values(self):
        from zope.schema.vocabulary import SimpleVocabulary
        choose = self._makeOne(values=[1, 2])
        self.assertTrue(isinstance(choose.vocabulary, SimpleVocabulary))
        self.assertEqual(sorted(choose.vocabulary.by_value.keys()), [1, 2])
        self.assertEqual(sorted(choose.source.by_value.keys()), [1, 2])

    def test_ctor_w_unicode_non_ascii_values(self):
        values = [u'K\xf6ln', u'D\xfcsseldorf', 'Bonn']
        choose = self._makeOne(values=values)
        self.assertEqual(sorted(choose.vocabulary.by_value.keys()),
                         sorted(values))
        self.assertEqual(sorted(choose.source.by_value.keys()),
                         sorted(values))
        self.assertEqual(
            sorted(choose.vocabulary.by_token.keys()),
            sorted([x.encode('ascii', 'backslashreplace').decode('ascii') for x in values]))


    def test_ctor_w_named_vocabulary(self):
        choose = self._makeOne(vocabulary="vocab")
        self.assertEqual(choose.vocabularyName, 'vocab')

    def test_ctor_w_preconstructed_vocabulary(self):
        v = _makeSampleVocabulary()
        choose = self._makeOne(vocabulary=v)
        self.assertTrue(choose.vocabulary is v)
        self.assertTrue(choose.vocabularyName is None)

    def test_bind_w_preconstructed_vocabulary(self):
        from zope.schema.interfaces import ValidationError
        from zope.schema.vocabulary import setVocabularyRegistry
        v = _makeSampleVocabulary()
        setVocabularyRegistry(_makeDummyRegistry(v))
        choose = self._makeOne(vocabulary='vocab')
        bound = choose.bind(None)
        self.assertEqual(bound.vocabulary, v)
        self.assertEqual(bound.vocabularyName, 'vocab')
        bound.default = 1
        self.assertEqual(bound.default, 1)

        def _provoke(bound):
            bound.default = 42

        self.assertRaises(ValidationError, _provoke, bound)

    def test_bind_w_voc_not_ICSB(self):
        from zope.interface import implementer
        from zope.schema.interfaces import ISource
        from zope.schema.interfaces import IBaseVocabulary

        @implementer(IBaseVocabulary)
        @implementer(ISource)
        class Vocab(object):
            def __init__(self):
                pass

        source = self._makeOne(vocabulary=Vocab())
        instance = DummyInstance()
        target = source.bind(instance)
        self.assertTrue(target.vocabulary is source.vocabulary)

    def test_bind_w_voc_is_ICSB(self):
        from zope.interface import implementer
        from zope.schema.interfaces import IContextSourceBinder
        from zope.schema.interfaces import ISource

        @implementer(IContextSourceBinder)
        @implementer(ISource)
        class Vocab(object):
            def __init__(self, context):
                self.context = context

            def __call__(self, context):
                return self.__class__(context)

        # Chicken-egg
        source = self._makeOne(vocabulary='temp')
        source.vocabulary = Vocab(source)
        source.vocabularyName = None
        instance = DummyInstance()
        target = source.bind(instance)
        self.assertEqual(target.vocabulary.context, instance)

    def test_bind_w_voc_is_ICSB_but_not_ISource(self):
        from zope.interface import implementer
        from zope.schema.interfaces import IContextSourceBinder

        @implementer(IContextSourceBinder)
        class Vocab(object):
            def __init__(self, context):
                self.context = context

            def __call__(self, context):
                return self.__class__(context)

        # Chicken-egg
        source = self._makeOne(vocabulary='temp')
        source.vocabulary = Vocab(source)
        source.vocabularyName = None
        instance = DummyInstance()
        self.assertRaises(ValueError, source.bind, instance)

    def test_fromUnicode_miss(self):
        from zope.schema.interfaces import ConstraintNotSatisfied

        flt = self._makeOne(values=(u'foo', u'bar', u'baz'))
        self.assertRaises(ConstraintNotSatisfied, flt.fromUnicode, u'')
        self.assertRaises(ConstraintNotSatisfied, flt.fromUnicode, u'abc')
        with self.assertRaises(ConstraintNotSatisfied) as exc:
            flt.fromUnicode(u'1.4G')

        cns = exc.exception
        self.assertIs(cns.field, flt)
        self.assertEqual(cns.value, u'1.4G')

    def test_fromUnicode_hit(self):

        flt = self._makeOne(values=(u'foo', u'bar', u'baz'))
        self.assertEqual(flt.fromUnicode(u'foo'), u'foo')
        self.assertEqual(flt.fromUnicode(u'bar'), u'bar')
        self.assertEqual(flt.fromUnicode(u'baz'), u'baz')

    def test__validate_int(self):
        from zope.schema.interfaces import ConstraintNotSatisfied
        choice = self._makeOne(values=[1, 3])
        choice._validate(1)  # doesn't raise
        choice._validate(3)  # doesn't raise
        self.assertRaises(ConstraintNotSatisfied, choice._validate, 4)

    def test__validate_string(self):

        from zope.schema.interfaces import ConstraintNotSatisfied
        choice = self._makeOne(values=['a', 'c'])
        choice._validate('a')  # doesn't raise
        choice._validate('c')  # doesn't raise
        choice._validate(u'c')  # doesn't raise
        self.assertRaises(ConstraintNotSatisfied, choice._validate, 'd')

    def test__validate_tuple(self):
        from zope.schema.interfaces import ConstraintNotSatisfied
        choice = self._makeOne(values=[(1, 2), (5, 6)])
        choice._validate((1, 2))  # doesn't raise
        choice._validate((5, 6))  # doesn't raise
        self.assertRaises(ConstraintNotSatisfied, choice._validate, [5, 6])
        self.assertRaises(ConstraintNotSatisfied, choice._validate, ())

    def test__validate_mixed(self):
        from zope.schema.interfaces import ConstraintNotSatisfied
        choice = self._makeOne(values=[1, 'b', (0.2,)])
        choice._validate(1)  # doesn't raise
        choice._validate('b')  # doesn't raise
        choice._validate((0.2,))  # doesn't raise
        self.assertRaises(ConstraintNotSatisfied, choice._validate, '1')
        self.assertRaises(ConstraintNotSatisfied, choice._validate, 0.2)

    def test__validate_w_named_vocabulary_invalid(self):
        choose = self._makeOne(vocabulary='vocab')
        self.assertRaises(ValueError, choose._validate, 42)

    def test__validate_w_named_vocabulary(self):
        from zope.schema.interfaces import ConstraintNotSatisfied
        from zope.schema.vocabulary import setVocabularyRegistry
        v = _makeSampleVocabulary()
        setVocabularyRegistry(_makeDummyRegistry(v))
        choose = self._makeOne(vocabulary='vocab')
        choose._validate(1)
        choose._validate(3)
        self.assertRaises(ConstraintNotSatisfied, choose._validate, 42)

    def test__validate_source_is_ICSB_unbound(self):
        from zope.interface import implementer
        from zope.schema.interfaces import IContextSourceBinder

        @implementer(IContextSourceBinder)
        class SampleContextSourceBinder(object):
            def __call__(self, context):
                raise AssertionError("This is not called")

        choice = self._makeOne(source=SampleContextSourceBinder())
        self.assertRaises(TypeError, choice.validate, 1)

    def test__validate_source_is_ICSB_bound(self):
        from zope.interface import implementer
        from zope.schema.interfaces import IContextSourceBinder
        from zope.schema.interfaces import ConstraintNotSatisfied
        from zope.schema.tests.test_vocabulary import _makeSampleVocabulary

        @implementer(IContextSourceBinder)
        class SampleContextSourceBinder(object):
            def __call__(self, context):
                return _makeSampleVocabulary()

        s = SampleContextSourceBinder()
        choice = self._makeOne(source=s)
        # raises not iterable with unbound field
        self.assertRaises(TypeError, choice.validate, 1)
        o = object()
        clone = choice.bind(o)
        clone._validate(1)
        clone._validate(3)
        self.assertRaises(ConstraintNotSatisfied, clone._validate, 42)


class URITests(EqualityTestsMixin,
               unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._field import URI
        return URI

    def _getTargetInterface(self):
        from zope.schema.interfaces import IURI
        return IURI

    def test_validate_wrong_types(self):
        from zope.schema.interfaces import WrongType
        from zope.schema._compat import non_native_string
        field = self._makeOne()
        self.assertRaises(WrongType, field.validate, non_native_string(''))
        self.assertRaises(WrongType, field.validate, 1)
        self.assertRaises(WrongType, field.validate, 1.0)
        self.assertRaises(WrongType, field.validate, ())
        self.assertRaises(WrongType, field.validate, [])
        self.assertRaises(WrongType, field.validate, {})
        self.assertRaises(WrongType, field.validate, set())
        self.assertRaises(WrongType, field.validate, frozenset())
        self.assertRaises(WrongType, field.validate, object())

    def test_validate_not_required(self):
        field = self._makeOne(required=False)
        field.validate('http://example.com/')
        field.validate(None)

    def test_validate_required(self):
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne()
        field.validate('http://example.com/')
        self.assertRaises(RequiredMissing, field.validate, None)

    def test_validate_not_a_uri(self):
        from zope.schema.interfaces import ConstraintNotSatisfied
        from zope.schema.interfaces import InvalidURI
        field = self._makeOne()
        with self.assertRaises(InvalidURI) as exc:
            field.validate('')

        invalid = exc.exception
        self.assertIs(invalid.field, field)
        self.assertEqual(invalid.value, '')

        self.assertRaises(InvalidURI, field.validate, 'abc')
        self.assertRaises(InvalidURI, field.validate, '\xab\xde')
        self.assertRaises(ConstraintNotSatisfied,
                          field.validate, 'http://example.com/\nDAV:')

    def test_fromUnicode_ok(self):

        field = self._makeOne()
        self.assertEqual(field.fromUnicode(u'http://example.com/'),
                         'http://example.com/')

    def test_fromUnicode_invalid(self):
        from zope.schema.interfaces import ConstraintNotSatisfied
        from zope.schema.interfaces import InvalidURI

        field = self._makeOne()
        self.assertRaises(InvalidURI, field.fromUnicode, u'')
        self.assertRaises(InvalidURI, field.fromUnicode, u'abc')
        self.assertRaises(ConstraintNotSatisfied,
                          field.fromUnicode, u'http://example.com/\nDAV:')


class DottedNameTests(EqualityTestsMixin,
                      unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._field import DottedName
        return DottedName

    def _getTargetInterface(self):
        from zope.schema.interfaces import IDottedName
        return IDottedName

    def test_ctor_defaults(self):
        dotted = self._makeOne()
        self.assertEqual(dotted.min_dots, 0)
        self.assertEqual(dotted.max_dots, None)

    def test_ctor_min_dots_invalid(self):
        self.assertRaises(ValueError, self._makeOne, min_dots=-1)

    def test_ctor_min_dots_valid(self):
        dotted = self._makeOne(min_dots=1)
        self.assertEqual(dotted.min_dots, 1)

    def test_ctor_max_dots_invalid(self):
        self.assertRaises(ValueError, self._makeOne, min_dots=2, max_dots=1)

    def test_ctor_max_dots_valid(self):
        dotted = self._makeOne(max_dots=2)
        self.assertEqual(dotted.max_dots, 2)

    def test_validate_wrong_types(self):
        from zope.schema.interfaces import WrongType
        from zope.schema._compat import non_native_string
        field = self._makeOne()
        self.assertRaises(WrongType, field.validate, non_native_string(''))
        self.assertRaises(WrongType, field.validate, 1)
        self.assertRaises(WrongType, field.validate, 1.0)
        self.assertRaises(WrongType, field.validate, ())
        self.assertRaises(WrongType, field.validate, [])
        self.assertRaises(WrongType, field.validate, {})
        self.assertRaises(WrongType, field.validate, set())
        self.assertRaises(WrongType, field.validate, frozenset())
        self.assertRaises(WrongType, field.validate, object())

    def test_validate_not_required(self):
        field = self._makeOne(required=False)
        field.validate('name')
        field.validate('dotted.name')
        field.validate(None)

    def test_validate_required(self):
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne()
        field.validate('name')
        field.validate('dotted.name')
        self.assertRaises(RequiredMissing, field.validate, None)

    def test_validate_w_min_dots(self):
        from zope.schema.interfaces import InvalidDottedName
        field = self._makeOne(min_dots=1)
        with self.assertRaises(InvalidDottedName) as exc:
            field.validate('name')
        invalid = exc.exception
        self.assertIs(invalid.field, field)
        self.assertEqual(invalid.value, 'name')

        field.validate('dotted.name')
        field.validate('moar.dotted.name')

    def test_validate_w_max_dots(self):
        from zope.schema.interfaces import InvalidDottedName
        field = self._makeOne(max_dots=1)
        field.validate('name')
        field.validate('dotted.name')
        with self.assertRaises(InvalidDottedName) as exc:
            field.validate('moar.dotted.name')

        invalid = exc.exception
        self.assertIs(invalid.field, field)
        self.assertEqual(invalid.value, 'moar.dotted.name')

    def test_validate_not_a_dotted_name(self):
        from zope.schema.interfaces import ConstraintNotSatisfied
        from zope.schema.interfaces import InvalidDottedName
        field = self._makeOne()
        self.assertRaises(InvalidDottedName, field.validate, '')
        self.assertRaises(InvalidDottedName, field.validate, '\xab\xde')
        self.assertRaises(ConstraintNotSatisfied,
                          field.validate, 'http://example.com/\nDAV:')

    def test_fromUnicode_dotted_name_ok(self):
        field = self._makeOne()
        self.assertEqual(field.fromUnicode(u'dotted.name'), 'dotted.name')

    def test_fromUnicode_invalid(self):
        from zope.schema.interfaces import ConstraintNotSatisfied
        from zope.schema.interfaces import InvalidDottedName

        field = self._makeOne()
        self.assertRaises(InvalidDottedName, field.fromUnicode, u'')
        with self.assertRaises(InvalidDottedName) as exc:
            field.fromUnicode(u'\u2603')
        invalid = exc.exception
        self.assertIs(invalid.field, field)
        self.assertEqual(invalid.value, u'\u2603')

        self.assertRaises(ConstraintNotSatisfied,
                          field.fromUnicode, u'http://example.com/\nDAV:')


class IdTests(EqualityTestsMixin,
              unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._field import Id
        return Id

    def _getTargetInterface(self):
        from zope.schema.interfaces import IId
        return IId

    def test_validate_wrong_types(self):
        from zope.schema.interfaces import WrongType
        from zope.schema._compat import non_native_string
        field = self._makeOne()
        self.assertRaises(WrongType, field.validate, non_native_string(''))
        self.assertRaises(WrongType, field.validate, 1)
        self.assertRaises(WrongType, field.validate, 1.0)
        self.assertRaises(WrongType, field.validate, ())
        self.assertRaises(WrongType, field.validate, [])
        self.assertRaises(WrongType, field.validate, {})
        self.assertRaises(WrongType, field.validate, set())
        self.assertRaises(WrongType, field.validate, frozenset())
        bad_value = object()
        with self.assertRaises(WrongType) as exc:
            field.validate(bad_value)

        wrong = exc.exception
        self.assertIs(wrong.field, field)
        self.assertEqual(wrong.value, bad_value)

    def test_validate_not_required(self):
        field = self._makeOne(required=False)
        field.validate('http://example.com/')
        field.validate('dotted.name')
        field.validate(None)

    def test_validate_required(self):
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne()
        field.validate('http://example.com/')
        field.validate('dotted.name')
        self.assertRaises(RequiredMissing, field.validate, None)

    def test_validate_not_a_uri(self):
        from zope.schema.interfaces import ConstraintNotSatisfied
        from zope.schema.interfaces import InvalidId
        field = self._makeOne()
        with self.assertRaises(InvalidId) as exc:
            field.validate('')

        invalid = exc.exception
        self.assertIs(invalid.field, field)
        self.assertEqual(invalid.value, '')

        self.assertRaises(InvalidId, field.validate, 'abc')
        self.assertRaises(InvalidId, field.validate, '\xab\xde')
        self.assertRaises(ConstraintNotSatisfied,
                          field.validate, 'http://example.com/\nDAV:')

    def test_fromUnicode_url_ok(self):

        field = self._makeOne()
        self.assertEqual(field.fromUnicode(u'http://example.com/'),
                         'http://example.com/')

    def test_fromUnicode_dotted_name_ok(self):

        field = self._makeOne()
        self.assertEqual(field.fromUnicode(u'dotted.name'), 'dotted.name')

    def test_fromUnicode_invalid(self):
        from zope.schema.interfaces import ConstraintNotSatisfied
        from zope.schema.interfaces import InvalidId

        field = self._makeOne()
        self.assertRaises(InvalidId, field.fromUnicode, u'')
        self.assertRaises(InvalidId, field.fromUnicode, u'abc')
        self.assertRaises(InvalidId, field.fromUnicode, u'\u2603')
        self.assertRaises(ConstraintNotSatisfied,
                          field.fromUnicode, u'http://example.com/\nDAV:')


class InterfaceFieldTests(EqualityTestsMixin,
                          unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._field import InterfaceField
        return InterfaceField

    def _getTargetInterface(self):
        from zope.schema.interfaces import IInterfaceField
        return IInterfaceField

    def test_validate_wrong_types(self):
        from datetime import date
        from zope.schema.interfaces import WrongType


        field = self._makeOne()
        with self.assertRaises(WrongType) as exc:
            field.validate(u'')

        wrong = exc.exception
        self.assertIs(wrong.field, field)
        self.assertEqual(wrong.value, u'')

        self.assertRaises(WrongType, field.validate, b'')
        self.assertRaises(WrongType, field.validate, 1)
        self.assertRaises(WrongType, field.validate, 1.0)
        self.assertRaises(WrongType, field.validate, ())
        self.assertRaises(WrongType, field.validate, [])
        self.assertRaises(WrongType, field.validate, {})
        self.assertRaises(WrongType, field.validate, set())
        self.assertRaises(WrongType, field.validate, frozenset())
        self.assertRaises(WrongType, field.validate, object())
        self.assertRaises(WrongType, field.validate, date.today())

    def test_validate_not_required(self):
        from zope.interface import Interface

        class DummyInterface(Interface):
            pass

        field = self._makeOne(required=False)
        field.validate(DummyInterface)
        field.validate(None)

    def test_validate_required(self):
        from zope.interface import Interface
        from zope.schema.interfaces import RequiredMissing

        class DummyInterface(Interface):
            pass

        field = self._makeOne(required=True)
        field.validate(DummyInterface)
        self.assertRaises(RequiredMissing, field.validate, None)


class CollectionTests(EqualityTestsMixin,
                      unittest.TestCase):

    _DEFAULT_UNIQUE = False

    def _getTargetClass(self):
        from zope.schema._field import Collection
        return Collection

    def _getTargetInterface(self):
        from zope.schema.interfaces import ICollection
        return ICollection

    _makeCollection = list


    def test_schema_defined_by_subclass(self):
        from zope import interface
        from zope.schema import Object
        from zope.schema.interfaces import WrongContainedType

        class IValueType(interface.Interface):
            "The value type schema"

        the_value_type = Object(IValueType)

        class Field(self._getTargetClass()):
            value_type = the_value_type

        field = Field()
        self.assertIs(field.value_type, the_value_type)

        # Empty collection is fine
        field.validate(self._makeCollection([]))

        # Collection with a non-implemented object is bad
        self.assertRaises(WrongContainedType, field.validate, self._makeCollection([object()]))

        # Actual implementation works
        @interface.implementer(IValueType)
        class ValueType(object):
            "The value type"


        field.validate(self._makeCollection([ValueType()]))

    def test_ctor_defaults(self):
        absc = self._makeOne()
        self.assertEqual(absc.value_type, None)
        self.assertEqual(absc.unique, self._DEFAULT_UNIQUE)

    def test_ctor_explicit(self):
        from zope.schema._bootstrapfields import Text
        text = Text()
        absc = self._makeOne(text, True)
        self.assertEqual(absc.value_type, text)
        self.assertEqual(absc.unique, True)

    def test_ctor_w_non_field_value_type(self):
        class NotAField(object):
            pass
        self.assertRaises(ValueError, self._makeOne, NotAField)

    def test_bind_wo_value_Type(self):
        absc = self._makeOne()
        context = object()
        bound = absc.bind(context)
        self.assertEqual(bound.context, context)
        self.assertEqual(bound.value_type, None)
        self.assertEqual(bound.unique, self._DEFAULT_UNIQUE)

    def test_bind_w_value_Type(self):
        from zope.schema._bootstrapfields import Text
        text = Text()
        absc = self._makeOne(text, True)
        context = object()
        bound = absc.bind(context)
        self.assertEqual(bound.context, context)
        self.assertEqual(isinstance(bound.value_type, Text), True)
        self.assertEqual(bound.value_type.context, context)
        self.assertEqual(bound.unique, True)

    def test__validate_wrong_contained_type(self):
        from zope.schema.interfaces import WrongContainedType
        from zope.schema._bootstrapfields import Text
        text = Text()
        absc = self._makeOne(text)
        with self.assertRaises(WrongContainedType) as exc:
            absc.validate(self._makeCollection([1]))

        wct = exc.exception
        self.assertIs(wct.field, absc)
        self.assertEqual(wct.value, self._makeCollection([1]))

    def test__validate_miss_uniqueness(self):
        from zope.schema.interfaces import NotUnique
        from zope.schema.interfaces import WrongType
        from zope.schema._bootstrapfields import Text

        text = Text()
        absc = self._makeOne(text, True)
        with self.assertRaises((NotUnique, WrongType)) as exc:
            absc.validate([u'a', u'a'])

        not_uniq = exc.exception
        self.assertIs(not_uniq.field, absc)
        self.assertEqual(not_uniq.value,
                         [u'a', u'a'])

    def test_validate_min_length(self):
        from zope.schema.interfaces import TooShort
        field = self._makeOne(min_length=2)
        field.validate(self._makeCollection((1, 2)))
        field.validate(self._makeCollection((1, 2, 3)))
        self.assertRaises(TooShort, field.validate, self._makeCollection())
        self.assertRaises(TooShort, field.validate, self._makeCollection((1,)))

    def test_validate_max_length(self):
        from zope.schema.interfaces import TooLong
        field = self._makeOne(max_length=2)
        field.validate(self._makeCollection())
        field.validate(self._makeCollection((1,)))
        field.validate(self._makeCollection((1, 2)))
        self.assertRaises(TooLong, field.validate, self._makeCollection((1, 2, 3, 4)))
        self.assertRaises(TooLong, field.validate, self._makeCollection((1, 2, 3)))

    def test_validate_min_length_and_max_length(self):
        from zope.schema.interfaces import TooLong
        from zope.schema.interfaces import TooShort
        field = self._makeOne(min_length=1, max_length=2)
        field.validate(self._makeCollection((1,)))
        field.validate(self._makeCollection((1, 2)))
        self.assertRaises(TooShort, field.validate, self._makeCollection())
        self.assertRaises(TooLong, field.validate, self._makeCollection((1, 2, 3)))

    def test_validate_not_required(self):
        field = self._makeOne(required=False)
        field.validate(self._makeCollection())
        field.validate(self._makeCollection((1, 2)))
        field.validate(self._makeCollection((3,)))
        field.validate(None)

    def test_validate_required(self):
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne()
        field.validate(self._makeCollection())
        field.validate(self._makeCollection((1, 2)))
        field.validate(self._makeCollection((3,)))
        field.validate(self._makeCollection())
        field.validate(self._makeCollection((1, 2)))
        field.validate(self._makeCollection((3,)))
        self.assertRaises(RequiredMissing, field.validate, None)


class SequenceTests(CollectionTests):

    def _getTargetClass(self):
        from zope.schema._field import Sequence
        return Sequence

    def _getTargetInterface(self):
        from zope.schema.interfaces import ISequence
        return ISequence

    def test_validate_wrong_types(self):
        from zope.schema.interfaces import WrongType

        field = self._makeOne()
        self.assertRaises(WrongType, field.validate, 1)
        self.assertRaises(WrongType, field.validate, 1.0)
        self.assertRaises(WrongType, field.validate, {})
        self.assertRaises(WrongType, field.validate, set())
        self.assertRaises(WrongType, field.validate, frozenset())
        self.assertRaises(WrongType, field.validate, object())

    def test_sequence(self):
        from zope.schema._field import abc

        class Sequence(abc.Sequence):
            def __getitem__(self, i):
                raise AssertionError("Not implemented")
            def __len__(self):
                return 0

        sequence = Sequence()
        field = self._makeOne()
        field.validate(sequence)

    def test_mutable_sequence(self):
        from zope.schema._field import abc

        class MutableSequence(abc.MutableSequence):
            def insert(self, item, ix):
                raise AssertionError("not implemented")
            def __getitem__(self, name):
                raise AssertionError("not implemented")
            def __iter__(self):
                return iter(())
            def __setitem__(self, name, value):
                raise AssertionError("Not implemented")
            def __len__(self):
                return 0
            __delitem__ = __getitem__


        sequence = MutableSequence()
        field = self._makeOne()
        field.validate(sequence)


class TupleTests(SequenceTests):

    _makeCollection = tuple

    def _getTargetClass(self):
        from zope.schema._field import Tuple
        return Tuple

    def _getTargetInterface(self):
        from zope.schema.interfaces import ITuple
        return ITuple

    def test_mutable_sequence(self):
        from zope.schema.interfaces import WrongType
        with self.assertRaises(WrongType):
            super(TupleTests, self).test_mutable_sequence()

    def test_sequence(self):
        from zope.schema.interfaces import WrongType
        with self.assertRaises(WrongType):
            super(TupleTests, self).test_sequence()

    def test_validate_wrong_types(self):
        from zope.schema.interfaces import WrongType
        field = self._makeOne()
        self.assertRaises(WrongType, field.validate, u'')
        self.assertRaises(WrongType, field.validate, b'')
        self.assertRaises(WrongType, field.validate, [])
        super(TupleTests, self).test_validate_wrong_types()


class MutableSequenceTests(SequenceTests):

    def _getTargetClass(self):
        from zope.schema._field import MutableSequence
        return MutableSequence

    def _getTargetInterface(self):
        from zope.schema.interfaces import IMutableSequence
        return IMutableSequence

    def test_validate_wrong_types(self):
        from zope.schema.interfaces import WrongType
        field = self._makeOne()
        self.assertRaises(WrongType, field.validate, u'')
        self.assertRaises(WrongType, field.validate, b'')
        self.assertRaises(WrongType, field.validate, ())
        super(MutableSequenceTests, self).test_validate_wrong_types()

    def test_sequence(self):
        from zope.schema.interfaces import WrongType
        with self.assertRaises(WrongType):
            super(MutableSequenceTests, self).test_sequence()


class ListTests(MutableSequenceTests):

    def _getTargetClass(self):
        from zope.schema._field import List
        return List

    def _getTargetInterface(self):
        from zope.schema.interfaces import IList
        return IList

    def test_mutable_sequence(self):
        from zope.schema.interfaces import WrongType
        with self.assertRaises(WrongType):
            super(ListTests, self).test_mutable_sequence()


class SetTests(CollectionTests):

    _DEFAULT_UNIQUE = True
    _makeCollection = set
    _makeWrongSet = frozenset

    def _getTargetClass(self):
        from zope.schema._field import Set
        return Set

    def _getTargetInterface(self):
        from zope.schema.interfaces import ISet
        return ISet

    def test_ctor_disallows_unique(self):
        self.assertRaises(TypeError, self._makeOne, unique=False)
        self._makeOne(unique=True) # restating the obvious is allowed
        self.assertTrue(self._makeOne().unique)

    def test_validate_wrong_types(self):
        from zope.schema.interfaces import WrongType

        field = self._makeOne()
        self.assertRaises(WrongType, field.validate, u'')
        self.assertRaises(WrongType, field.validate, b'')
        self.assertRaises(WrongType, field.validate, 1)
        self.assertRaises(WrongType, field.validate, 1.0)
        self.assertRaises(WrongType, field.validate, ())
        self.assertRaises(WrongType, field.validate, [])
        self.assertRaises(WrongType, field.validate, {})
        self.assertRaises(WrongType, field.validate, self._makeWrongSet())
        self.assertRaises(WrongType, field.validate, object())


class FrozenSetTests(SetTests):

    _makeCollection = frozenset
    _makeWrongSet = set

    def _getTargetClass(self):
        from zope.schema._field import FrozenSet
        return FrozenSet

    def _getTargetInterface(self):
        from zope.schema.interfaces import IFrozenSet
        return IFrozenSet


class ObjectTests(EqualityTestsMixin,
                  unittest.TestCase):

    def setUp(self):
        from zope.event import subscribers
        self._before = subscribers[:]

    def tearDown(self):
        from zope.event import subscribers
        subscribers[:] = self._before

    def _getTargetClass(self):
        from zope.schema._field import Object
        return Object

    def _getTargetInterface(self):
        from zope.schema.interfaces import IObject
        return IObject

    def _makeOneFromClass(self, cls, schema=None, *args, **kw):
        if schema is None:
            schema = self._makeSchema()
        return super(ObjectTests, self)._makeOneFromClass(cls, schema, *args, **kw)

    def _makeSchema(self, **kw):
        from zope.interface import Interface
        from zope.interface.interface import InterfaceClass
        return InterfaceClass('ISchema', (Interface,), kw)

    def _getErrors(self, f, *args, **kw):
        from zope.schema.interfaces import WrongContainedType
        with self.assertRaises(WrongContainedType) as e:
            f(*args, **kw)
        return e.exception.args[0]

    def _makeCycles(self):
        from zope.interface import Interface
        from zope.interface import implementer
        from zope.schema import Object
        from zope.schema import List
        from zope.schema._messageid import _

        class IUnit(Interface):
            """A schema that participate to a cycle"""
            boss = Object(
                schema=Interface,
                title=_("Boss"),
                description=_("Boss description"),
                required=False,
                )
            members = List(
                value_type=Object(schema=Interface),
                title=_("Member List"),
                description=_("Member list description"),
                required=False,
                )

        class IPerson(Interface):
            """A schema that participate to a cycle"""
            unit = Object(
                schema=IUnit,
                title=_("Unit"),
                description=_("Unit description"),
                required=False,
                )

        IUnit['boss'].schema = IPerson
        IUnit['members'].value_type.schema = IPerson

        @implementer(IUnit)
        class Unit(object):
            def __init__(self, person, person_list):
                self.boss = person
                self.members = person_list

        @implementer(IPerson)
        class Person(object):
            def __init__(self, unit):
                self.unit = unit

        return IUnit, Person, Unit

    def test_class_conforms_to_IObject(self):
        from zope.interface.verify import verifyClass
        from zope.schema.interfaces import IObject
        verifyClass(IObject, self._getTargetClass())

    def test_instance_conforms_to_IObject(self):
        from zope.interface.verify import verifyObject
        from zope.schema.interfaces import IObject
        verifyObject(IObject, self._makeOne())

    def test_ctor_w_bad_schema(self):
        from zope.schema.interfaces import WrongType
        self.assertRaises(WrongType, self._makeOne, object())

    def test_validate_not_required(self):
        schema = self._makeSchema()
        objf = self._makeOne(schema, required=False)
        objf.validate(None)  # doesn't raise

    def test_validate_required(self):
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne(required=True)
        self.assertRaises(RequiredMissing, field.validate, None)

    def test__validate_w_empty_schema(self):
        from zope.interface import Interface
        objf = self._makeOne(Interface)
        objf.validate(object())  # doesn't raise

    def test__validate_w_value_not_providing_schema(self):
        from zope.schema.interfaces import SchemaNotProvided
        from zope.schema._bootstrapfields import Text
        schema = self._makeSchema(foo=Text(), bar=Text())
        objf = self._makeOne(schema)
        bad_value = object()
        with self.assertRaises(SchemaNotProvided) as exc:
            objf.validate(bad_value)

        not_provided = exc.exception
        self.assertIs(not_provided.field, objf)
        self.assertIs(not_provided.value, bad_value)
        self.assertEqual(not_provided.args, (schema, bad_value), )

    def test__validate_w_value_providing_schema_but_missing_fields(self):
        from zope.interface import implementer
        from zope.schema.interfaces import SchemaNotFullyImplemented
        from zope.schema.interfaces import SchemaNotCorrectlyImplemented
        from zope.schema._bootstrapfields import Text
        schema = self._makeSchema(foo=Text(), bar=Text())

        @implementer(schema)
        class Broken(object):
            pass

        objf = self._makeOne(schema)
        broken = Broken()
        with self.assertRaises(SchemaNotCorrectlyImplemented) as exc:
            objf.validate(broken)

        wct = exc.exception
        self.assertIs(wct.field, objf)
        self.assertIs(wct.value, broken)
        self.assertEqual(wct.invariant_errors, [])
        self.assertEqual(
            sorted(wct.schema_errors),
            ['bar', 'foo']
        )
        for name in ('foo', 'bar'):
            error = wct.schema_errors[name]
            self.assertIsInstance(error,
                                  SchemaNotFullyImplemented)
            self.assertEqual(schema[name], error.field)
            self.assertIsNone(error.value)

        # The legacy arg[0] errors list
        errors = self._getErrors(objf.validate, Broken())
        self.assertEqual(len(errors), 2)
        errors = sorted(errors,
                        key=lambda x: (type(x).__name__, str(x.args[0])))
        err = errors[0]
        self.assertIsInstance(err, SchemaNotFullyImplemented)
        nested = err.args[0]
        self.assertIsInstance(nested, AttributeError)
        self.assertIn("'bar'", str(nested))
        err = errors[1]
        self.assertIsInstance(err, SchemaNotFullyImplemented)
        nested = err.args[0]
        self.assertIsInstance(nested, AttributeError)
        self.assertIn("'foo'", str(nested))

    def test__validate_w_value_providing_schema_but_invalid_fields(self):
        from zope.interface import implementer
        from zope.schema.interfaces import SchemaNotCorrectlyImplemented
        from zope.schema.interfaces import RequiredMissing
        from zope.schema.interfaces import WrongType
        from zope.schema._bootstrapfields import Text
        from zope.schema._compat import text_type
        schema = self._makeSchema(foo=Text(), bar=Text())

        @implementer(schema)
        class Broken(object):
            foo = None
            bar = 1

        objf = self._makeOne(schema)
        broken = Broken()
        with self.assertRaises(SchemaNotCorrectlyImplemented) as exc:
            objf.validate(broken)

        wct = exc.exception
        self.assertIs(wct.field, objf)
        self.assertIs(wct.value, broken)
        self.assertEqual(wct.invariant_errors, [])
        self.assertEqual(
            sorted(wct.schema_errors),
            ['bar', 'foo']
        )
        self.assertIsInstance(wct.schema_errors['foo'], RequiredMissing)
        self.assertIsInstance(wct.schema_errors['bar'], WrongType)

        # The legacy arg[0] errors list
        errors = self._getErrors(objf.validate, Broken())
        self.assertEqual(len(errors), 2)
        errors = sorted(errors, key=lambda x: type(x).__name__)
        err = errors[0]
        self.assertIsInstance(err, RequiredMissing)
        self.assertEqual(err.args, ('foo',))
        err = errors[1]
        self.assertIsInstance(err, WrongType)
        self.assertEqual(err.args, (1, text_type, 'bar'))

    def test__validate_w_value_providing_schema(self):
        from zope.interface import implementer
        from zope.schema._bootstrapfields import Text
        from zope.schema._field import Choice

        schema = self._makeSchema(
            foo=Text(),
            bar=Text(),
            baz=Choice(values=[1, 2, 3]),
        )

        @implementer(schema)
        class OK(object):
            foo = u'Foo'
            bar = u'Bar'
            baz = 2
        objf = self._makeOne(schema)
        objf.validate(OK())  # doesn't raise

    def test_validate_w_cycles(self):
        IUnit, Person, Unit = self._makeCycles()
        field = self._makeOne(schema=IUnit)
        person1 = Person(None)
        person2 = Person(None)
        unit = Unit(person1, [person1, person2])
        person1.unit = unit
        person2.unit = unit
        field.validate(unit)  # doesn't raise

    def test_validate_w_cycles_object_not_valid(self):
        from zope.schema.interfaces import WrongContainedType
        IUnit, Person, Unit = self._makeCycles()
        field = self._makeOne(schema=IUnit)
        person1 = Person(None)
        person2 = Person(None)
        person3 = Person(DummyInstance())
        unit = Unit(person3, [person1, person2])
        person1.unit = unit
        person2.unit = unit
        self.assertRaises(WrongContainedType, field.validate, unit)

    def test_validate_w_cycles_collection_not_valid(self):
        from zope.schema.interfaces import WrongContainedType
        IUnit, Person, Unit = self._makeCycles()
        field = self._makeOne(schema=IUnit)
        person1 = Person(None)
        person2 = Person(None)
        person3 = Person(DummyInstance())
        unit = Unit(person1, [person2, person3])
        person1.unit = unit
        person2.unit = unit
        self.assertRaises(WrongContainedType, field.validate, unit)

    def test_set_emits_IBOAE(self):
        from zope.event import subscribers
        from zope.interface import implementer
        from zope.schema.interfaces import IBeforeObjectAssignedEvent
        from zope.schema._bootstrapfields import Text
        from zope.schema._field import Choice

        schema = self._makeSchema(
            foo=Text(),
            bar=Text(),
            baz=Choice(values=[1, 2, 3]),
        )

        @implementer(schema)
        class OK(object):
            foo = u'Foo'
            bar = u'Bar'
            baz = 2
        log = []
        subscribers.append(log.append)
        objf = self._makeOne(schema, __name__='field')
        inst = DummyInstance()
        value = OK()
        objf.set(inst, value)
        self.assertEqual(inst.field is value, True)
        self.assertEqual(len(log), 5)
        self.assertEqual(IBeforeObjectAssignedEvent.providedBy(log[-1]), True)
        self.assertEqual(log[-1].object, value)
        self.assertEqual(log[-1].name, 'field')
        self.assertEqual(log[-1].context, inst)

    def test_set_allows_IBOAE_subscr_to_replace_value(self):
        from zope.event import subscribers
        from zope.interface import implementer
        from zope.schema._bootstrapfields import Text
        from zope.schema._field import Choice

        schema = self._makeSchema(
            foo=Text(),
            bar=Text(),
            baz=Choice(values=[1, 2, 3]),
        )

        @implementer(schema)
        class OK(object):
            def __init__(self, foo=u'Foo', bar=u'Bar', baz=2):
                self.foo = foo
                self.bar = bar
                self.baz = baz
        ok1 = OK()
        ok2 = OK(u'Foo2', u'Bar2', 3)
        log = []
        subscribers.append(log.append)

        def _replace(event):
            event.object = ok2
        subscribers.append(_replace)
        objf = self._makeOne(schema, __name__='field')
        inst = DummyInstance()
        self.assertEqual(len(log), 4)
        objf.set(inst, ok1)
        self.assertEqual(inst.field is ok2, True)
        self.assertEqual(len(log), 5)
        self.assertEqual(log[-1].object, ok2)
        self.assertEqual(log[-1].name, 'field')
        self.assertEqual(log[-1].context, inst)

    def test_validates_invariants_by_default(self):
        from zope.interface import invariant
        from zope.interface import Interface
        from zope.interface import implementer
        from zope.interface import Invalid
        from zope.schema import Text
        from zope.schema import Bytes

        class ISchema(Interface):

            foo = Text()
            bar = Bytes()

            @invariant
            def check_foo(self):
                if self.foo == u'bar':
                    raise Invalid("Foo is not valid")

            @invariant
            def check_bar(self):
                if self.bar == b'foo':
                    raise Invalid("Bar is not valid")

        @implementer(ISchema)
        class O(object):
            foo = u''
            bar = b''


        field = self._makeOne(ISchema)
        inst = O()

        # Fine at first
        field.validate(inst)

        inst.foo = u'bar'
        errors = self._getErrors(field.validate, inst)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].args[0], "Foo is not valid")

        del inst.foo
        inst.bar = b'foo'
        errors = self._getErrors(field.validate, inst)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].args[0], "Bar is not valid")

        # Both invalid
        inst.foo = u'bar'
        errors = self._getErrors(field.validate, inst)
        self.assertEqual(len(errors), 2)
        errors.sort(key=lambda i: i.args)
        self.assertEqual(errors[0].args[0], "Bar is not valid")
        self.assertEqual(errors[1].args[0], "Foo is not valid")

        # We can specifically ask for invariants to be turned off.
        field = self._makeOne(ISchema, validate_invariants=False)
        field.validate(inst)

    def test_schema_defined_by_subclass(self):
        from zope import interface
        from zope.schema.interfaces import SchemaNotProvided

        class IValueType(interface.Interface):
            "The value type schema"

        class Field(self._getTargetClass()):
            schema = IValueType

        field = Field()
        self.assertIs(field.schema, IValueType)

        # Non implementation is bad
        self.assertRaises(SchemaNotProvided, field.validate, object())

        # Actual implementation works
        @interface.implementer(IValueType)
        class ValueType(object):
            "The value type"


        field.validate(ValueType())

    def test_bound_field_of_collection_with_choice(self):
        # https://github.com/zopefoundation/zope.schema/issues/17
        from zope.interface import Interface, implementer
        from zope.interface import Attribute

        from zope.schema import Choice, Object, Set
        from zope.schema.fieldproperty import FieldProperty
        from zope.schema.interfaces import IContextSourceBinder
        from zope.schema.interfaces import WrongContainedType
        from zope.schema.interfaces import SchemaNotCorrectlyImplemented
        from zope.schema.vocabulary import SimpleVocabulary


        @implementer(IContextSourceBinder)
        class EnumContext(object):
            def __call__(self, context):
                return SimpleVocabulary.fromValues(list(context))

        class IMultipleChoice(Interface):
            choices = Set(value_type=Choice(source=EnumContext()))
            # Provide a regular attribute to prove that binding doesn't
            # choke. NOTE: We don't actually verify the existence of this attribute.
            non_field = Attribute("An attribute")

        @implementer(IMultipleChoice)
        class Choices(object):

            def __init__(self, choices):
                self.choices = choices

            def __iter__(self):
                # EnumContext calls this to make the vocabulary.
                # Fields of the schema of the IObject are bound to the value being
                # validated.
                return iter(range(5))

        class IFavorites(Interface):
            fav = Object(title=u"Favorites number", schema=IMultipleChoice)


        @implementer(IFavorites)
        class Favorites(object):
            fav = FieldProperty(IFavorites['fav'])

        # must not raise
        good_choices = Choices({1, 3})
        IFavorites['fav'].validate(good_choices)

        # Ranges outside the context fail
        bad_choices = Choices({1, 8})
        with self.assertRaises(WrongContainedType) as exc:
            IFavorites['fav'].validate(bad_choices)

        e = exc.exception
        self.assertEqual(IFavorites['fav'], e.field)
        self.assertEqual(bad_choices, e.value)

        # Validation through field property
        favorites = Favorites()
        favorites.fav = good_choices

        # And validation through a field that wants IFavorites
        favorites_field = Object(IFavorites)
        favorites_field.validate(favorites)

        # Check the field property error
        with self.assertRaises(SchemaNotCorrectlyImplemented) as exc:
            favorites.fav = bad_choices

        e = exc.exception
        self.assertEqual(IFavorites['fav'], e.field)
        self.assertEqual(bad_choices, e.value)
        self.assertEqual(['choices'], list(e.schema_errors))


class MappingTests(EqualityTestsMixin,
                   unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._field import Mapping
        return Mapping

    def _getTargetInterface(self):
        from zope.schema.interfaces import IMapping
        return IMapping

    def test_ctor_key_type_not_IField(self):
        self.assertRaises(ValueError, self._makeOne, key_type=object())

    def test_ctor_value_type_not_IField(self):
        self.assertRaises(ValueError, self._makeOne, value_type=object())

    def test_validate_wrong_types(self):
        from zope.schema.interfaces import WrongType

        field = self._makeOne()
        self.assertRaises(WrongType, field.validate, u'')
        self.assertRaises(WrongType, field.validate, u'')
        self.assertRaises(WrongType, field.validate, 1)
        self.assertRaises(WrongType, field.validate, 1.0)
        self.assertRaises(WrongType, field.validate, ())
        self.assertRaises(WrongType, field.validate, [])
        self.assertRaises(WrongType, field.validate, set())
        self.assertRaises(WrongType, field.validate, frozenset())
        self.assertRaises(WrongType, field.validate, object())

    def test_validate_not_required(self):
        field = self._makeOne(required=False)
        field.validate({})
        field.validate({1: 'b', 2: 'd'})
        field.validate({3: 'a'})
        field.validate(None)

    def test_validate_required(self):
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne()
        field.validate({})
        field.validate({1: 'b', 2: 'd'})
        field.validate({3: 'a'})
        self.assertRaises(RequiredMissing, field.validate, None)

    def test_validate_invalid_key_type(self):
        from zope.schema.interfaces import WrongContainedType
        from zope.schema._bootstrapfields import Int
        field = self._makeOne(key_type=Int())
        field.validate({})
        field.validate({1: 'b', 2: 'd'})
        field.validate({3: 'a'})
        with self.assertRaises(WrongContainedType) as exc:
            field.validate({'a': 1})

        wct = exc.exception
        self.assertIs(wct.field, field)
        self.assertEqual(wct.value, {'a': 1})

    def test_validate_invalid_value_type(self):
        from zope.schema.interfaces import WrongContainedType
        from zope.schema._bootstrapfields import Int
        field = self._makeOne(value_type=Int())
        field.validate({})
        field.validate({'b': 1, 'd': 2})
        field.validate({'a': 3})
        with self.assertRaises(WrongContainedType) as exc:
            field.validate({1: 'a'})

        wct = exc.exception
        self.assertIs(wct.field, field)
        self.assertEqual(wct.value, {1: 'a'})

    def test_validate_min_length(self):
        from zope.schema.interfaces import TooShort
        field = self._makeOne(min_length=1)
        field.validate({1: 'a'})
        field.validate({1: 'a', 2: 'b'})
        self.assertRaises(TooShort, field.validate, {})

    def test_validate_max_length(self):
        from zope.schema.interfaces import TooLong
        field = self._makeOne(max_length=1)
        field.validate({})
        field.validate({1: 'a'})
        self.assertRaises(TooLong, field.validate, {1: 'a', 2: 'b'})
        self.assertRaises(TooLong, field.validate, {1: 'a', 2: 'b', 3: 'c'})

    def test_validate_min_length_and_max_length(self):
        from zope.schema.interfaces import TooLong
        from zope.schema.interfaces import TooShort
        field = self._makeOne(min_length=1, max_length=2)
        field.validate({1: 'a'})
        field.validate({1: 'a', 2: 'b'})
        self.assertRaises(TooShort, field.validate, {})
        self.assertRaises(TooLong, field.validate, {1: 'a', 2: 'b', 3: 'c'})

    def test_bind_binds_key_and_value_types(self):
        from zope.schema import Int
        field = self._makeOne(key_type=Int(), value_type=Int())
        context = DummyInstance()
        field2 = field.bind(context)
        self.assertEqual(field2.key_type.context, context)
        self.assertEqual(field2.value_type.context, context)

    def test_mapping(self):
        from zope.schema._field import abc

        class Mapping(abc.Mapping):

            def __getitem__(self, name):
                raise AssertionError("not implemented")
            def __iter__(self):
                return iter(())
            def __len__(self):
                return 0


        mm = Mapping()
        field = self._makeOne()
        field.validate(mm)

    def test_mutable_mapping(self):
        from zope.schema._field import abc

        class MutableMapping(abc.MutableMapping):

            def __getitem__(self, name):
                raise AssertionError("not implemented")
            def __iter__(self):
                return iter(())
            def __setitem__(self, name, value):
                raise AssertionError("Not implemented")
            def __len__(self):
                return 0
            __delitem__ = __getitem__

        mm = MutableMapping()
        field = self._makeOne()
        field.validate(mm)


class MutableMappingTests(MappingTests):

    def _getTargetClass(self):
        from zope.schema._field import MutableMapping
        return MutableMapping

    def _getTargetInterface(self):
        from zope.schema.interfaces import IMutableMapping
        return IMutableMapping

    def test_mapping(self):
        from zope.schema.interfaces import WrongType
        with self.assertRaises(WrongType):
            super(MutableMappingTests, self).test_mapping()


class DictTests(MutableMappingTests):

    def _getTargetClass(self):
        from zope.schema._field import Dict
        return Dict

    def _getTargetInterface(self):
        from zope.schema.interfaces import IDict
        return IDict

    def test_mutable_mapping(self):
        from zope.schema.interfaces import WrongType
        with self.assertRaises(WrongType):
            super(DictTests, self).test_mutable_mapping()


class DummyInstance(object):
    pass


def _makeSampleVocabulary():
    from zope.interface import implementer
    from zope.schema.interfaces import IVocabulary

    @implementer(IVocabulary)
    class SampleVocabulary(object):

        def __iter__(self):
            raise AssertionError("Not implemented")

        def __contains__(self, value):
            return 0 <= value < 10

        def __len__(self): # pragma: no cover
            return 10

        def getTerm(self, value):
            raise AssertionError("Not implemented")

    return SampleVocabulary()


def _makeDummyRegistry(v):
    from zope.schema.vocabulary import VocabularyRegistry

    class DummyRegistry(VocabularyRegistry):
        def __init__(self, vocabulary):
            VocabularyRegistry.__init__(self)
            self._vocabulary = vocabulary

        def get(self, object, name):
            return self._vocabulary
    return DummyRegistry(v)


def test_suite():
    import zope.schema._field
    suite = unittest.defaultTestLoader.loadTestsFromName(__name__)
    suite.addTests(doctest.DocTestSuite(
        zope.schema._field,
        optionflags=doctest.ELLIPSIS
    ))
    return suite

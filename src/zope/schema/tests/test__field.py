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

    def setUp(self):
        from zope.schema.vocabulary import _clear
        _clear()

    def tearDown(self):
        from zope.schema.vocabulary import _clear
        _clear()

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
        self.assertEqual(sorted(choose.source.by_value.keys()), [1, 2])

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

    def test__validate_int(self):
        from zope.schema.interfaces import ConstraintNotSatisfied
        choice = self._makeOne(values=[1, 3])
        choice._validate(1) #doesn't raise
        choice._validate(3) #doesn't raise
        self.assertRaises(ConstraintNotSatisfied, choice._validate, 4)

    def test__validate_string(self):
        from zope.schema._compat import u
        from zope.schema.interfaces import ConstraintNotSatisfied
        choice = self._makeOne(values=['a', 'c'])
        choice._validate('a') #doesn't raise
        choice._validate('c') #doesn't raise
        choice._validate(u('c')) #doesn't raise
        self.assertRaises(ConstraintNotSatisfied, choice._validate, 'd')

    def test__validate_tuple(self):
        from zope.schema.interfaces import ConstraintNotSatisfied
        choice = self._makeOne(values=[(1, 2), (5, 6)])
        choice._validate((1, 2)) #doesn't raise
        choice._validate((5, 6)) #doesn't raise
        self.assertRaises(ConstraintNotSatisfied, choice._validate, [5, 6])
        self.assertRaises(ConstraintNotSatisfied, choice._validate, ())

    def test__validate_mixed(self):
        from zope.schema.interfaces import ConstraintNotSatisfied
        choice = self._makeOne(values=[1, 'b', (0.2,)])
        choice._validate(1) #doesn't raise
        choice._validate('b') #doesn't raise
        choice._validate((0.2,)) #doesn't raise
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
                pass
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


class DummyInstance(object):
    pass


def _makeSampleVocabulary():
    from zope.interface import implementer
    from zope.schema.interfaces import IVocabulary

    class SampleTerm(object):
        pass

    @implementer(IVocabulary)
    class SampleVocabulary(object):

        def __iter__(self):
            return iter([self.getTerm(x) for x in range(0, 10)])

        def __contains__(self, value):
            return 0 <= value < 10

        def __len__(self):
            return 10

        def getTerm(self, value):
            if value in self:
                t = SampleTerm()
                t.value = value
                t.double = 2 * value
                return t
            raise LookupError("no such value: %r" % value)

    return SampleVocabulary()

def _makeDummyRegistry(v):
    from zope.schema.vocabulary import VocabularyRegistry
    class DummyRegistry(VocabularyRegistry):
        def __init__(self, vocabulary):
            self._vocabulary = vocabulary
        def get(self, object, name):
            return self._vocabulary
    return DummyRegistry(v)


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


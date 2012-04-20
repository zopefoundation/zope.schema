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
"""Test of the Choice field.
"""
import unittest


class _Base(unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema import Choice
        return Choice

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)


class Value_ChoiceFieldTests(_Base):
    """Tests of the Choice Field using values."""

    def test_create_vocabulary(self):
        choice = self._makeOne(values=[1, 3])
        self.assertEqual([term.value for term in choice.vocabulary], [1, 3])

    def test_validate_int(self):
        from zope.schema.interfaces import ConstraintNotSatisfied
        choice = self._makeOne(values=[1, 3])
        choice.validate(1)
        choice.validate(3)
        self.assertRaises(ConstraintNotSatisfied, choice.validate, 4)

    def test_validate_string(self):
        from six import u
        from zope.schema.interfaces import ConstraintNotSatisfied
        choice = self._makeOne(values=['a', 'c'])
        choice.validate('a')
        choice.validate('c')
        choice.validate(u('c'))
        self.assertRaises(ConstraintNotSatisfied, choice.validate, 'd')

    def test_validate_tuple(self):
        from zope.schema.interfaces import ConstraintNotSatisfied
        choice = self._makeOne(values=[(1, 2), (5, 6)])
        choice.validate((1, 2))
        choice.validate((5, 6))
        self.assertRaises(ConstraintNotSatisfied, choice.validate, [5, 6])
        self.assertRaises(ConstraintNotSatisfied, choice.validate, ())

    def test_validate_mixed(self):
        from zope.schema.interfaces import ConstraintNotSatisfied
        choice = self._makeOne(values=[1, 'b', (0.2,)])
        choice.validate(1)
        choice.validate('b')
        choice.validate((0.2,))
        self.assertRaises(ConstraintNotSatisfied, choice.validate, '1')
        self.assertRaises(ConstraintNotSatisfied, choice.validate, 0.2)


class Vocabulary_ChoiceFieldTests(_Base):
    """Tests of the Choice Field using vocabularies."""

    def setUp(self):
        from zope.schema.vocabulary import _clear
        _clear()

    def tearDown(self):
        from zope.schema.vocabulary import _clear
        _clear()

    def _getTargetClass(self):
        from zope.schema import Choice
        return Choice

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_preconstructed_vocabulary(self):
        from zope.schema.interfaces import ValidationError
        from zope.schema.tests.test_vocabulary import _makeSampleVocabulary
        v = _makeSampleVocabulary()
        field = self._makeOne(vocabulary=v)
        self.assertTrue(field.vocabulary is v)
        self.assertTrue(field.vocabularyName is None)
        bound = field.bind(None)
        self.assertTrue(bound.vocabulary is v)
        self.assertTrue(bound.vocabularyName is None)
        bound.default = 1
        self.assertEqual(bound.default, 1)
        self.assertRaises(ValidationError, setattr, bound, "default", 42)

    def test_constructed_vocabulary(self):
        from zope.schema.interfaces import ValidationError
        from zope.schema.vocabulary import setVocabularyRegistry
        from zope.schema.tests.test_vocabulary import _makeDummyRegistry
        setVocabularyRegistry(_makeDummyRegistry())
        field = self._makeOne(vocabulary="vocab")
        self.assertTrue(field.vocabulary is None)
        self.assertEqual(field.vocabularyName, "vocab")
        o = object()
        bound = field.bind(o)
        bound.default = 1
        self.assertEqual(bound.default, 1)
        self.assertRaises(ValidationError, setattr, bound, "default", 42)

    def test_create_vocabulary(self):
        from zope.schema.vocabulary import setVocabularyRegistry
        from zope.schema.tests.test_vocabulary import _makeDummyRegistry
        setVocabularyRegistry(_makeDummyRegistry())
        field = self._makeOne(vocabulary="vocab")
        o = object()
        bound = field.bind(o)
        self.assertEqual([term.value for term in bound.vocabulary],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_undefined_vocabulary(self):
        choice = self._makeOne(vocabulary="unknown")
        self.assertRaises(ValueError, choice.validate, "value")


class ContextSourceBinder_ChoiceFieldTests(_Base):
    """Tests of the Choice Field using IContextSourceBinder as source."""

    def setUp(self):
        from zope.schema.vocabulary import _clear
        _clear()

    def tearDown(self):
        from zope.schema.vocabulary import _clear
        _clear()

    def test_validate_source(self):
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
        clone.validate(1)
        clone.validate(3)
        self.assertRaises(ConstraintNotSatisfied, clone.validate, 42)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(Vocabulary_ChoiceFieldTests),
        unittest.makeSuite(Value_ChoiceFieldTests),
        unittest.makeSuite(ContextSourceBinder_ChoiceFieldTests),
    ))

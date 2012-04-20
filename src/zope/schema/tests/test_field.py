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
"""Generic field tests
"""
import unittest


class FieldTestBase(object):

    def _getTargetClass(self):
        raise NotImplementedError

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_bind(self):
        from six import u
        from zope.interface import Interface
        field = self._makeOne(
            __name__ = 'x',
            title=u('Not required field'), description=u(''),
            readonly=False, required=False)

        field.interface = Interface
        field.setTaggedValue('a', 'b')

        class C(object):
            x=None

        c = C()
        field2 = field.bind(c)

        self.assertEqual(field2.context, c)
        self.assertEqual(field.queryTaggedValue('a'),
                         field2.queryTaggedValue('a'))
        for n in ('__class__', '__name__', '__doc__', 'title', 'description',
                  'readonly', 'required', 'interface'):
            self.assertEqual(getattr(field2, n), getattr(field, n), n)

    def testValidate(self):
        from six import u
        field = self._makeOne(
            title=u('Not required field'), description=u(''),
            readonly=False, required=False)
        field.validate(None)
        field.validate('foo')
        field.validate(1)
        field.validate(0)
        field.validate('')

    def testValidateRequired(self):
        from six import u
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne(
            title=u('Required field'), description=u(''),
            readonly=False, required=True)
        field.validate('foo')
        field.validate(1)
        field.validate(0)
        field.validate('')

        self.assertRaises(RequiredMissing, field.validate, None)

class CollectionFieldTestBase(FieldTestBase):

    def test_bind_binds_value_type(self):
        from six import u
        from zope.schema import Int
        field = self._makeOne(
            __name__ = 'x',
            title=u('Not required field'), description=u(''),
            readonly=False, required=False,
            value_type=Int(),
            )

        class C(object):
            x=None

        c = C()
        field2 = field.bind(c)

        self.assertEqual(field2.value_type.context, c)

class FieldTest(unittest.TestCase, FieldTestBase):
    """Test generic Field."""

    def _getTargetClass(self):
        from zope.schema import Field
        return Field

    def test__doc__(self):
        from six import u
        field = self._makeOne(title=u("test fiield"),
                     description=(
                         u("To make sure that\n"
                           "doc strings are working correctly\n")
                         )
                     )
        self.assertEqual(
            field.__doc__,
            u("test fiield\n\n"
              "To make sure that\n"
              "doc strings are working correctly\n")
            )

    def testOrdering(self):

        from zope.interface import Interface

        class S1(Interface):
            a = self._makeOne()
            b = self._makeOne()

        self.assertTrue(S1['a'].order < S1['b'].order)

        class S2(Interface):
            b = self._makeOne()
            a = self._makeOne()

        self.assertTrue(S2['a'].order > S2['b'].order)

    def testConstraint(self):
        from six import u
        from zope.schema import Int
        from zope.schema.interfaces import ConstraintNotSatisfied
        def isodd(x):
            return x % 2 == 1

        i = Int(title=u('my constrained integer'),
                constraint=isodd)

        i.validate(11)
        self.assertRaises(ConstraintNotSatisfied, i.validate, 10)

    def testSimpleDefaultFactory(self):
        from zope.schema import Int
        field = Int(defaultFactory=lambda: 42)
        self.assertEqual(field.default, 42)

        # The default factory always wins against a default value.
        field = Int(default=41, defaultFactory=lambda: 42)
        self.assertEqual(field.default, 42)

    def testContextAwareDefaultFactory(self):
        from zope.interface import provider
        from zope.schema import Int
        from zope.schema.interfaces import IContextAwareDefaultFactory
        @provider(IContextAwareDefaultFactory)
        def getAnswerToUniverse(context):
            if context is None:
                return 0
            return context.answer

        field = Int(defaultFactory=getAnswerToUniverse)
        self.assertEqual(field.default, 0)

        class Context(object):
            answer = 42

        bound = field.bind(Context())
        self.assertEqual(bound.default, 42)

    def testBadValueDefaultFactory(self):
        from zope.schema import Int
        from zope.schema.interfaces import WrongType
        field = Int(defaultFactory=lambda: '42')
        self.assertRaises(WrongType, lambda: field.default)

class FieldDefaultBehaviour(unittest.TestCase):
    def test_required_defaults_to_true(self):
        from zope.schema import Field
        from six import u
        class MyField(Field):
            pass
        field = MyField(title=u('my'))
        self.assertTrue(field.required)

def test_suite():
    from doctest import DocTestSuite
    import re
    from zope.schema.tests import py3_checker
    from zope.testing import renormalizing
    checker = renormalizing.RENormalizing([
        (re.compile(r" with base 10: '125.6'"),
                    r': 125.6')
        ])
    checker = checker + py3_checker
    return unittest.TestSuite((
        unittest.makeSuite(FieldTest),
        unittest.makeSuite(FieldDefaultBehaviour),
        DocTestSuite("zope.schema._field", checker=py3_checker),
        DocTestSuite("zope.schema._bootstrapfields",checker=checker),
        ))

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
"""Field Properties tests
"""

from unittest import TestCase, TestSuite, main, makeSuite

from six import u, b
from zope.interface import Interface
from zope.schema import Float, Text, Bytes
from zope.schema.interfaces import ValidationError
from zope.schema.fieldproperty import (FieldProperty,
                                       FieldPropertyStoredThroughField)


class I(Interface):

    title = Text(description=u("Short summary"), default=u('say something'))
    weight = Float(min=0.0)
    code = Bytes(min_length=6, max_length=6, default=b('xxxxxx'))
    date = Float(title=u('Date'), readonly=True)


class C(object):

    title = FieldProperty(I['title'])
    weight = FieldProperty(I['weight'])
    code = FieldProperty(I['code'])
    date = FieldProperty(I['date'])


class Test(TestCase):
    klass = C

    def test_basic(self):
        c = self.klass()
        self.assertEqual(c.title, u('say something'))
        self.assertEqual(c.weight, None)
        self.assertEqual(c.code, b('xxxxxx'))
        self.assertRaises(ValidationError, setattr, c, 'title', b('foo'))
        self.assertRaises(ValidationError, setattr, c, 'weight', b('foo'))
        self.assertRaises(ValidationError, setattr, c, 'weight', -1.0)
        self.assertRaises(ValidationError, setattr, c, 'weight', 2)
        self.assertRaises(ValidationError, setattr, c, 'code', -1)
        self.assertRaises(ValidationError, setattr, c, 'code', b('xxxx'))
        self.assertRaises(ValidationError, setattr, c, 'code', u('xxxxxx'))

        c.title = u('c is good')
        c.weight = 10.0
        c.code = b('abcdef')

        self.assertEqual(c.title, u('c is good'))
        self.assertEqual(c.weight, 10)
        self.assertEqual(c.code, b('abcdef'))

    def test_readonly(self):
        c = self.klass()
        # The date should be only settable once
        c.date = 0.0
        # Setting the value a second time should fail.
        self.assertRaises(ValueError, setattr, c, 'date', 1.0)


class D(object):

    title = FieldPropertyStoredThroughField(I['title'])
    weight = FieldPropertyStoredThroughField(I['weight'])
    code = FieldPropertyStoredThroughField(I['code'])
    date = FieldPropertyStoredThroughField(I['date'])


class TestStoredThroughField(Test):
    klass = D


def test_suite():
    return TestSuite((
        makeSuite(Test),
        makeSuite(TestStoredThroughField),
        ))

if __name__ == '__main__':
    main(defaultTest='test_suite')

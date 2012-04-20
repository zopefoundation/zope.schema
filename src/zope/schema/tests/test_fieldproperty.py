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

import unittest


class Test(unittest.TestCase):

    def _getSchema(self):
        from six import b
        from six import u
        from zope.interface import Interface
        from zope.schema import Bytes
        from zope.schema import Float
        from zope.schema import Text

        class Schema(Interface):
            title = Text(description=u("Short summary"),
                         default=u('say something'))
            weight = Float(min=0.0)
            code = Bytes(min_length=6, max_length=6, default=b('xxxxxx'))
            date = Float(title=u('Date'), readonly=True)

        return Schema

    def _getTargetClass(self):
        from zope.schema.fieldproperty import FieldProperty
        schema = self._getSchema()

        class Klass(object):
            title = FieldProperty(schema['title'])
            weight = FieldProperty(schema['weight'])
            code = FieldProperty(schema['code'])
            date = FieldProperty(schema['date'])

        return Klass

    def _makeOne(self):
        return self._getTargetClass()()

    def test_basic(self):
        from six import b
        from six import u
        from zope.schema.interfaces import ValidationError
        c = self._makeOne()
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
        c = self._makeOne()
        # The date should be only settable once
        c.date = 0.0
        # Setting the value a second time should fail.
        self.assertRaises(ValueError, setattr, c, 'date', 1.0)


class TestStoredThroughField(Test):

    def _getTargetClass(self):
        schema = self._getSchema()

        class Klass(object):
            from zope.schema.fieldproperty import \
                FieldPropertyStoredThroughField
            title = FieldPropertyStoredThroughField(schema['title'])
            weight = FieldPropertyStoredThroughField(schema['weight'])
            code = FieldPropertyStoredThroughField(schema['code'])
            date = FieldPropertyStoredThroughField(schema['date'])

        return Klass


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(Test),
        unittest.makeSuite(TestStoredThroughField),
        ))

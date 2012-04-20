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
"""Dictionary field tests
"""
import unittest

from zope.schema.tests.test_field import FieldTestBase


class DictTest(unittest.TestCase, FieldTestBase):
    """Test the Dict Field."""

    def _getTargetClass(self):
        from zope.schema import Dict
        return Dict

    def testValidate(self):
        from six import u
        field = self._makeOne(title=u('Dict field'),
                     description=u(''), readonly=False, required=False)
        field.validate(None)
        field.validate({})
        field.validate({1: 'foo'})
        field.validate({'a': 1})

    def testValidateRequired(self):
        from six import u
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne(title=u('Dict field'),
                     description=u(''), readonly=False, required=True)
        field.validate({})
        field.validate({1: 'foo'})
        field.validate({'a': 1})

        self.assertRaises(RequiredMissing, field.validate, None)

    def testValidateMinValues(self):
        from six import u
        from zope.schema.interfaces import TooShort
        field = self._makeOne(title=u('Dict field'),
                     description=u(''), readonly=False, required=False,
                     min_length=1)
        field.validate(None)
        field.validate({1: 'a'})
        field.validate({1: 'a', 2: 'b'})

        self.assertRaises(TooShort, field.validate, {})

    def testValidateMaxValues(self):
        from six import u
        from zope.schema.interfaces import TooLong
        field = self._makeOne(title=u('Dict field'),
                     description=u(''), readonly=False, required=False,
                     max_length=1)
        field.validate(None)
        field.validate({})
        field.validate({1: 'a'})

        self.assertRaises(TooLong, field.validate, {1: 'a', 2: 'b'})
        self.assertRaises(TooLong, field.validate, {1: 'a', 2: 'b', 3: 'c'})

    def testValidateMinValuesAndMaxValues(self):
        from six import u
        from zope.schema.interfaces import TooLong
        from zope.schema.interfaces import TooShort
        field = self._makeOne(title=u('Dict field'),
                     description=u(''), readonly=False, required=False,
                     min_length=1, max_length=2)
        field.validate(None)
        field.validate({1: 'a'})
        field.validate({1: 'a', 2: 'b'})

        self.assertRaises(TooShort, field.validate, {})
        self.assertRaises(TooLong, field.validate, {1: 'a', 2: 'b', 3: 'c'})

    def testValidateValueType(self):
        from six import u
        from zope.schema import Int
        from zope.schema.interfaces import WrongContainedType
        field = self._makeOne(title=u('Dict field'),
                     description=u(''), readonly=False, required=False,
                     value_type=Int())
        field.validate(None)
        field.validate({'a': 5})
        field.validate({'a': 2, 'b': 3})

        self.assertRaises(WrongContainedType, field.validate, {1: ''} )
        self.assertRaises(WrongContainedType, field.validate, {1: 3.14159} )
        self.assertRaises(WrongContainedType, field.validate, {'a': ()} )

    def testValidateKeyTypes(self):
        from six import u
        from zope.schema import Int
        from zope.schema.interfaces import WrongContainedType
        field = self._makeOne(title=u('Dict field'),
                     description=u(''), readonly=False, required=False,
                     key_type=Int())
        field.validate(None)
        field.validate({5: 'a'})
        field.validate({2: 'a', 2: 'b'})

        self.assertRaises(WrongContainedType, field.validate, {'': 1} )
        self.assertRaises(WrongContainedType, field.validate, {3.14159: 1} )
        self.assertRaises(WrongContainedType, field.validate, {(): 'a'} )


    def test_bind_binds_key_and_value_types(self):
        from six import u
        from zope.schema import Int
        field = self._makeOne(
            __name__ = 'x',
            title=u('Not required field'), description=u(''),
            readonly=False, required=False,
            key_type=Int(),
            value_type=Int(),
            )

        class C(object):
            x=None

        c = C()
        field2 = field.bind(c)

        self.assertEqual(field2.key_type.context, c)
        self.assertEqual(field2.value_type.context, c)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(DictTest),
    ))

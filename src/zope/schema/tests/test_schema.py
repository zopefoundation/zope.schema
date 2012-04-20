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
"""Schema field tests
"""
import unittest

def _makeSchema():
    from zope.schema._compat import b
    from zope.schema._compat import u
    from zope.interface import Interface
    from zope.schema import Bytes

    class ISchemaTest(Interface):
        title = Bytes(
            title=u("Title"),
            description=u("Title"),
            default=b(""),
            required=True)
        description = Bytes(
            title=u("Description"),
            description=u("Description"),
            default=b(""),
            required=True)
        spam = Bytes(
            title=u("Spam"),
            description=u("Spam"),
            default=b(""),
            required=True)
    return ISchemaTest

def _makeDerivedSchema(base=None):
    from zope.schema._compat import b
    from zope.schema._compat import u
    from zope.schema import Bytes
    if base is None:
        base = _makeSchema()

    class ISchemaTestSubclass(base):
        foo = Bytes(
            title=u('Foo'),
            description=u('Fooness'),
            default=b(""),
            required=False)
    return ISchemaTestSubclass


class Test_getFields(unittest.TestCase):

    def _callFUT(self, schema):
        from zope.schema import getFields
        return getFields(schema)

    def test_simple(self):
        fields = self._callFUT(_makeSchema())

        self.assertTrue('title' in fields)
        self.assertTrue('description' in fields)
        self.assertTrue('spam' in fields)

        # test whether getName() has the right value
        for key, value in fields.items():
            self.assertEqual(key, value.getName())

    def test_derived(self):
        fields = self._callFUT(_makeDerivedSchema())

        self.assertTrue('title' in fields)
        self.assertTrue('description' in fields)
        self.assertTrue('spam' in fields)
        self.assertTrue('foo' in fields)

        # test whether getName() has the right value
        for key, value in fields.items():
            self.assertEqual(key, value.getName())


class Test_getFieldsInOrder(unittest.TestCase):

    def _callFUT(self, schema):
        from zope.schema import getFieldsInOrder
        return getFieldsInOrder(schema)

    def test_simple(self):
        fields = self._callFUT(_makeSchema())
        field_names = [name for name, field in fields]
        self.assertEqual(field_names, ['title', 'description', 'spam'])
        for key, value in fields:
            self.assertEqual(key, value.getName())

    def test_derived(self):
        fields = self._callFUT(_makeDerivedSchema())
        field_names = [name for name, field in fields]
        self.assertEqual(field_names, ['title', 'description', 'spam', 'foo'])
        for key, value in fields:
            self.assertEqual(key, value.getName())


class Test_getFieldNames(unittest.TestCase):

    def _callFUT(self, schema):
        from zope.schema import getFieldNames
        return getFieldNames(schema)

    def test_simple(self):
        names = self._callFUT(_makeSchema())
        self.assertEqual(len(names),3)
        self.assertTrue('title' in names)
        self.assertTrue('description' in names)
        self.assertTrue('spam' in names)

    def test_derived(self):
        names = self._callFUT(_makeDerivedSchema())
        self.assertEqual(len(names),4)
        self.assertTrue('title' in names)
        self.assertTrue('description' in names)
        self.assertTrue('spam' in names)
        self.assertTrue('foo' in names)


class Test_getFieldNamesInOrder(unittest.TestCase):

    def _callFUT(self, schema):
        from zope.schema import getFieldNamesInOrder
        return getFieldNamesInOrder(schema)

    def test_simple(self):
        names = self._callFUT(_makeSchema())
        self.assertEqual(names, ['title', 'description', 'spam'])

    def test_derived(self):
        names = self._callFUT(_makeDerivedSchema())
        self.assertEqual(names, ['title', 'description', 'spam', 'foo'])


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(Test_getFields),
        unittest.makeSuite(Test_getFieldsInOrder),
        unittest.makeSuite(Test_getFieldNames),
        unittest.makeSuite(Test_getFieldNamesInOrder),
    ))

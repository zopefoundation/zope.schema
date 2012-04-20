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


class SchemaTest(unittest.TestCase):

    def _makeSchema(self):
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

    def _makeDerivedSchema(self):
        from zope.schema._compat import b
        from zope.schema._compat import u
        from zope.schema import Bytes

        class ISchemaTestSubclass(self._makeSchema()):
            foo = Bytes(
                title=u('Foo'),
                description=u('Fooness'),
                default=b(""),
                required=False)
        return ISchemaTestSubclass

    def test_getFieldNames(self):
        from zope.schema import getFieldNames
        names = getFieldNames(self._makeSchema())
        self.assertEqual(len(names),3)
        self.assertTrue('title' in names)
        self.assertTrue('description' in names)
        self.assertTrue('spam' in names)

    def test_getFieldNamesAll(self):
        from zope.schema import getFieldNames
        names = getFieldNames(self._makeDerivedSchema())
        self.assertEqual(len(names),4)
        self.assertTrue('title' in names)
        self.assertTrue('description' in names)
        self.assertTrue('spam' in names)
        self.assertTrue('foo' in names)

    def test_getFields(self):
        from zope.schema import getFields
        fields = getFields(self._makeSchema())

        self.assertTrue('title' in fields)
        self.assertTrue('description' in fields)
        self.assertTrue('spam' in fields)

        # test whether getName() has the right value
        for key, value in fields.items():
            self.assertEqual(key, value.getName())

    def test_getFieldsAll(self):
        from zope.schema import getFields
        fields = getFields(self._makeDerivedSchema())

        self.assertTrue('title' in fields)
        self.assertTrue('description' in fields)
        self.assertTrue('spam' in fields)
        self.assertTrue('foo' in fields)

        # test whether getName() has the right value
        for key, value in fields.items():
            self.assertEqual(key, value.getName())

    def test_getFieldsInOrder(self):
        from zope.schema import getFieldsInOrder
        fields = getFieldsInOrder(self._makeSchema())
        field_names = [name for name, field in fields]
        self.assertEqual(field_names, ['title', 'description', 'spam'])
        for key, value in fields:
            self.assertEqual(key, value.getName())

    def test_getFieldsInOrderAll(self):
        from zope.schema import getFieldsInOrder
        fields = getFieldsInOrder(self._makeDerivedSchema())
        field_names = [name for name, field in fields]
        self.assertEqual(field_names, ['title', 'description', 'spam', 'foo'])
        for key, value in fields:
            self.assertEqual(key, value.getName())

    def test_getFieldsNamesInOrder(self):
        from zope.schema import getFieldNamesInOrder
        names = getFieldNamesInOrder(self._makeSchema())
        self.assertEqual(names, ['title', 'description', 'spam'])

    def test_getFieldsNamesInOrderAll(self):
        from zope.schema import getFieldNamesInOrder
        names = getFieldNamesInOrder(self._makeDerivedSchema())
        self.assertEqual(names, ['title', 'description', 'spam', 'foo'])


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(SchemaTest),
    ))

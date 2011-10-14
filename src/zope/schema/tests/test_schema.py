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
from unittest import TestCase, main, makeSuite
from six import u, b
from zope.interface import Interface
from zope.schema import Bytes
from zope.schema import getFields, getFieldsInOrder
from zope.schema import getFieldNames, getFieldNamesInOrder

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

class ISchemaTestSubclass(ISchemaTest):
    foo = Bytes(
        title=u('Foo'),
        description=u('Fooness'),
        default=b(""),
        required=False)


class SchemaTest(TestCase):

    def test_getFieldNames(self):
        names = getFieldNames(ISchemaTest)
        self.assertEqual(len(names),3)
        self.assertTrue('title' in names)
        self.assertTrue('description' in names)
        self.assertTrue('spam' in names)

    def test_getFieldNamesAll(self):
        names = getFieldNames(ISchemaTestSubclass)
        self.assertEqual(len(names),4)
        self.assertTrue('title' in names)
        self.assertTrue('description' in names)
        self.assertTrue('spam' in names)
        self.assertTrue('foo' in names)

    def test_getFields(self):
        fields = getFields(ISchemaTest)

        self.assertTrue('title' in fields)
        self.assertTrue('description' in fields)
        self.assertTrue('spam' in fields)

        # test whether getName() has the right value
        for key, value in fields.items():
            self.assertEqual(key, value.getName())

    def test_getFieldsAll(self):
        fields = getFields(ISchemaTestSubclass)

        self.assertTrue('title' in fields)
        self.assertTrue('description' in fields)
        self.assertTrue('spam' in fields)
        self.assertTrue('foo' in fields)

        # test whether getName() has the right value
        for key, value in fields.items():
            self.assertEqual(key, value.getName())

    def test_getFieldsInOrder(self):
        fields = getFieldsInOrder(ISchemaTest)
        field_names = [name for name, field in fields]
        self.assertEqual(field_names, ['title', 'description', 'spam'])
        for key, value in fields:
            self.assertEqual(key, value.getName())

    def test_getFieldsInOrderAll(self):
        fields = getFieldsInOrder(ISchemaTestSubclass)
        field_names = [name for name, field in fields]
        self.assertEqual(field_names, ['title', 'description', 'spam', 'foo'])
        for key, value in fields:
            self.assertEqual(key, value.getName())

    def test_getFieldsNamesInOrder(self):
        names = getFieldNamesInOrder(ISchemaTest)
        self.assertEqual(names, ['title', 'description', 'spam'])

    def test_getFieldsNamesInOrderAll(self):
        names = getFieldNamesInOrder(ISchemaTestSubclass)
        self.assertEqual(names, ['title', 'description', 'spam', 'foo'])

def test_suite():
    return makeSuite(SchemaTest)

if __name__ == '__main__':
    main(defaultTest='test_suite')

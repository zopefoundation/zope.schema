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
"""Boolean field tests
"""
import unittest

from zope.schema.tests.test_field import FieldTestBase


class BoolTest(FieldTestBase):
    """Test the Bool Field."""

    def _getTargetClass(self):
        from zope.schema import Bool
        return Bool

    def testValidate(self):
        from six import u
        field = self._makeOne(title=u('Bool field'), description=u(''),
                     readonly=False, required=False)
        field.validate(None)
        field.validate(True)
        field.validate(False)

    def testValidateRequired(self):
        from six import u
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne(title=u('Bool field'), description=u(''),
                     readonly=False, required=True)
        field.validate(True)
        field.validate(False)

        self.assertRaises(RequiredMissing, field.validate, None)

    def testIBoolIsMoreImportantThanIFromUnicode(self):
        from six import u
        from zope.interface import Interface
        from zope.interface.adapter import AdapterRegistry
        from zope.schema.interfaces import IBool
        from zope.schema.interfaces import IFromUnicode
        registry = AdapterRegistry()

        def adapt_bool(context):
            return 'bool'

        def adapt_from_unicode(context):
            return 'unicode'

        class IAdaptTo(Interface):
            pass

        registry.register((IBool,), IAdaptTo, u(''), adapt_bool)
        registry.register((IFromUnicode,), IAdaptTo, u(''), adapt_from_unicode)

        field = self._makeOne(title=u('Bool field'), description=u(''),
                     readonly=False, required=True)

        self.assertEqual('bool', registry.queryAdapter(field, IAdaptTo))


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(BoolTest),
    ))

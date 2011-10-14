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
from unittest import main, makeSuite

from six import u
from zope.schema import Bool
from zope.schema.interfaces import RequiredMissing, IBool, IFromUnicode
from zope.schema.tests.test_field import FieldTestBase
import zope.interface.adapter
import zope.interface


class BoolTest(FieldTestBase):
    """Test the Bool Field."""

    _Field_Factory = Bool

    def testValidate(self):
        field = Bool(title=u('Bool field'), description=u(''),
                     readonly=False, required=False)
        field.validate(None)
        field.validate(True)
        field.validate(False)

    def testValidateRequired(self):
        field = Bool(title=u('Bool field'), description=u(''),
                     readonly=False, required=True)
        field.validate(True)
        field.validate(False)

        self.assertRaises(RequiredMissing, field.validate, None)

    def testIBoolIsMoreImportantThanIFromUnicode(self):
        registry = zope.interface.adapter.AdapterRegistry()

        def adapt_bool(context):
            return 'bool'

        def adapt_from_unicode(context):
            return 'unicode'

        class IAdaptTo(zope.interface.Interface):
            pass

        registry.register((IBool,), IAdaptTo, u(''), adapt_bool)
        registry.register((IFromUnicode,), IAdaptTo, u(''), adapt_from_unicode)

        field = Bool(title=u('Bool field'), description=u(''),
                     readonly=False, required=True)

        self.assertEqual('bool', registry.queryAdapter(field, IAdaptTo))


def test_suite():
    return makeSuite(BoolTest)

if __name__ == '__main__':
    main(defaultTest='test_suite')

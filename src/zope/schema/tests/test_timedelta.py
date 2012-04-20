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
"""Timedelta Field tests
"""
import unittest

from zope.schema.tests.test_field import FieldTestBase


class TimedeltaTest(unittest.TestCase, FieldTestBase):
    """Test the Timedelta Field."""

    def _getTargetClass(self):
        from zope.schema import Timedelta
        return Timedelta

    def testInterface(self):
        from zope.interface.verify import verifyObject
        from zope.schema.interfaces import ITimedelta
        verifyObject(ITimedelta, self._makeOne())

    def testValidate(self):
        from datetime import timedelta
        from six import u
        field = self._makeOne(title=u('Timedelta field'),
                                    description=u(''),
                                    readonly=False, required=False)
        field.validate(None)
        field.validate(timedelta(minutes=15))

    def testValidateRequired(self):
        from datetime import timedelta
        from six import u
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne(title=u('Timedelta field'), description=u(''),
                                    readonly=False, required=True)
        field.validate(timedelta(minutes=15))

        self.assertRaises(RequiredMissing, field.validate, None)

    def testValidateMin(self):
        from datetime import timedelta
        from six import u
        from zope.schema.interfaces import TooSmall
        t1 = timedelta(hours=2)
        t2 = timedelta(hours=3)
        field = self._makeOne(title=u('Timedelta field'),
                                    description=u(''),
                                    readonly=False, required=False, min=t1)
        field.validate(None)
        field.validate(t1)
        field.validate(t2)

        self.assertRaises(TooSmall, field.validate, timedelta(hours=1))

    def testValidateMax(self):
        from datetime import timedelta
        from six import u
        from zope.schema.interfaces import TooBig
        t1 = timedelta(minutes=1)
        t2 = timedelta(minutes=2)
        t3 = timedelta(minutes=3)
        field = self._makeOne(title=u('Timedelta field'),
                                    description=u(''),
                                    readonly=False, required=False, max=t2)
        field.validate(None)
        field.validate(t1)
        field.validate(t2)

        self.assertRaises(TooBig, field.validate, t3)

    def testValidateMinAndMax(self):
        from datetime import timedelta
        from six import u
        from zope.schema.interfaces import TooBig
        from zope.schema.interfaces import TooSmall
        t1 = timedelta(days=1)
        t2 = timedelta(days=2)
        t3 = timedelta(days=3)
        t4 = timedelta(days=4)
        t5 = timedelta(days=5)

        field = self._makeOne(title=u('Timedelta field'),
                                    description=u(''),
                                    readonly=False, required=False,
                                    min=t2, max=t4)
        field.validate(None)
        field.validate(t2)
        field.validate(t3)
        field.validate(t4)

        self.assertRaises(TooSmall, field.validate, t1)
        self.assertRaises(TooBig, field.validate, t5)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(TimedeltaTest),
    ))

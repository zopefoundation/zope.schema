##############################################################################
#
# Copyright (c) 2012 Zope Foundation and Contributors.
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
import unittest

try:
    compare = cmp
except NameError:
    def compare(a, b):
        return -1 if a < b else (0 if a == b else 1)

class ValidationErrorTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._bootstrapinterfaces import ValidationError
        return ValidationError

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_doc(self):
        class Derived(self._getTargetClass()):
            """DERIVED"""
        inst = Derived()
        self.assertEqual(inst.doc(), 'DERIVED')

    def test___cmp___no_args(self):
        ve = self._makeOne()
        self.assertEqual(compare(ve, object()), -1)

    def test___cmp___hit(self):
        left = self._makeOne('abc')
        right = self._makeOne('def')
        self.assertEqual(compare(left, right), -1)
        self.assertEqual(compare(left, left), 0)
        self.assertEqual(compare(right, left), 1)

    def test___eq___no_args(self):
        ve = self._makeOne()
        self.assertEqual(ve == object(), False)

    def test___eq___w_args(self):
        left = self._makeOne('abc')
        right = self._makeOne('def')
        self.assertEqual(left == right, False)
        self.assertEqual(left == left, True)
        self.assertEqual(right == right, True)

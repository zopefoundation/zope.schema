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


class ValidatedPropertyTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._bootstrapfields import ValidatedProperty
        return ValidatedProperty

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test___set___not_missing_w_check(self):
        _checked = []
        def _check(inst, value):
            _checked.append((inst, value))
        class Test(DummyInst):
            _prop = None
            prop = self._makeOne('_prop', _check)
        inst = Test()
        inst.prop = 'PROP'
        self.assertEqual(inst._prop, 'PROP')
        self.assertEqual(_checked, [(inst, 'PROP')])

    def test___set___not_missing_wo_check(self):
        class Test(DummyInst):
            _prop = None
            prop = self._makeOne('_prop')
        inst = Test(ValueError)
        def _provoke(inst):
            inst.prop = 'PROP'
        self.assertRaises(ValueError, _provoke, inst)
        self.assertEqual(inst._prop, None)

    def test___set___w_missing_wo_check(self):
        class Test(DummyInst):
            _prop = None
            prop = self._makeOne('_prop')
        inst = Test(ValueError)
        inst.prop = DummyInst.missing_value
        self.assertEqual(inst._prop, DummyInst.missing_value)

    def test___get__(self):
        class Test(DummyInst):
            _prop = None
            prop = self._makeOne('_prop')
        inst = Test()
        inst._prop = 'PROP'
        self.assertEqual(inst.prop, 'PROP')


class DefaultPropertyTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._bootstrapfields import DefaultProperty
        return DefaultProperty

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test___get___wo_defaultFactory_miss(self):
        class Test(DummyInst):
            _prop = None
            prop = self._makeOne('_prop')
        inst = Test()
        inst.defaultFactory = None
        def _provoke(inst):
            return inst.prop
        self.assertRaises(KeyError, _provoke, inst)

    def test___get___wo_defaultFactory_hit(self):
        class Test(DummyInst):
            _prop = None
            prop = self._makeOne('_prop')
        inst = Test()
        inst.defaultFactory = None
        inst._prop = 'PROP'
        self.assertEqual(inst.prop, 'PROP')

    def test___get___w_defaultFactory_not_ICAF_no_check(self):
        class Test(DummyInst):
            _prop = None
            prop = self._makeOne('_prop')
        inst = Test(ValueError)
        def _factory():
            return 'PROP'
        inst.defaultFactory = _factory
        def _provoke(inst):
            return inst.prop
        self.assertRaises(ValueError, _provoke, inst)

    def test___get___w_defaultFactory_w_ICAF_w_check(self):
        from zope.interface import directlyProvides
        from zope.schema._bootstrapinterfaces \
            import IContextAwareDefaultFactory
        _checked = []
        def _check(inst, value):
            _checked.append((inst, value))
        class Test(DummyInst):
            _prop = None
            prop = self._makeOne('_prop', _check)
        inst = Test(ValueError)
        inst.context = object()
        _called_with = []
        def _factory(context):
            _called_with.append(context)
            return 'PROP'
        directlyProvides(_factory, IContextAwareDefaultFactory)
        inst.defaultFactory = _factory
        self.assertEqual(inst.prop, 'PROP')
        self.assertEqual(_checked, [(inst, 'PROP')])
        self.assertEqual(_called_with, [inst.context])


class DummyInst(object):
    missing_value = object()

    def __init__(self, exc=None):
        self._exc = exc

    def validate(self, value):
        if self._exc is not None:
            raise self._exc()


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(ValidatedPropertyTests),
        unittest.makeSuite(DefaultPropertyTests),
    ))

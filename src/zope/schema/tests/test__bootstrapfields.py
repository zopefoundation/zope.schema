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


class FieldTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.schema._bootstrapfields import Field
        return Field

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        from zope.schema._compat import u
        field = self._makeOne()
        self.assertEqual(field.__name__, u(''))
        self.assertEqual(field.__doc__, u(''))
        self.assertEqual(field.title, u(''))
        self.assertEqual(field.description, u(''))
        self.assertEqual(field.required, True)
        self.assertEqual(field.readonly, False)
        self.assertEqual(field.constraint(object()), True)
        self.assertEqual(field.default, None)
        self.assertEqual(field.defaultFactory, None)
        self.assertEqual(field.missing_value, None)
        self.assertEqual(field.context, None)

    def test_ctor_w_title_wo_description(self):
        from zope.schema._compat import u
        field = self._makeOne(u('TITLE'))
        self.assertEqual(field.__name__, u(''))
        self.assertEqual(field.__doc__, u('TITLE'))
        self.assertEqual(field.title, u('TITLE'))
        self.assertEqual(field.description, u(''))

    def test_ctor_wo_title_w_description(self):
        from zope.schema._compat import u
        field = self._makeOne(description=u('DESC'))
        self.assertEqual(field.__name__, u(''))
        self.assertEqual(field.__doc__, u('DESC'))
        self.assertEqual(field.title, u(''))
        self.assertEqual(field.description, u('DESC'))

    def test_ctor_w_both_title_and_description(self):
        from zope.schema._compat import u
        field = self._makeOne(u('TITLE'), u('DESC'), u('NAME'))
        self.assertEqual(field.__name__, u('NAME'))
        self.assertEqual(field.__doc__, u('TITLE\n\nDESC'))
        self.assertEqual(field.title, u('TITLE'))
        self.assertEqual(field.description, u('DESC'))

    def test_ctor_order_madness(self):
        klass = self._getTargetClass()
        order_before = klass.order
        field = self._makeOne()
        order_after = klass.order
        self.assertEqual(order_after, order_before + 1)
        self.assertEqual(field.order, order_after)

    def test_explicit_required_readonly_missingValue(self):
        obj = object()
        field = self._makeOne(required=False, readonly=True, missing_value=obj)
        self.assertEqual(field.required, False)
        self.assertEqual(field.readonly, True)
        self.assertEqual(field.missing_value, obj)

    def test_explicit_constraint_default(self):
        _called_with = []
        obj = object()
        def _constraint(value):
            _called_with.append(value)
            return value is obj
        field = self._makeOne(required=False,
                              readonly=True,
                              constraint=_constraint,
                              default=obj,
                             )
        self.assertEqual(field.required, False)
        self.assertEqual(field.readonly, True)
        self.assertEqual(_called_with, [obj])
        self.assertEqual(field.constraint(self), False)
        self.assertEqual(_called_with, [obj, self])
        self.assertEqual(field.default, obj)

    def test_explicit_defaultFactory(self):
        _called_with = []
        obj = object()
        def _constraint(value):
            _called_with.append(value)
            return value is obj
        def _factory():
            return obj
        field = self._makeOne(required=False,
                              readonly=True,
                              constraint=_constraint,
                              defaultFactory=_factory,
                             )
        self.assertEqual(field.required, False)
        self.assertEqual(field.readonly, True)
        self.assertEqual(field.constraint(self), False)
        self.assertEqual(_called_with, [self])
        self.assertEqual(field.default, obj)
        self.assertEqual(_called_with, [self, obj])
        self.assertEqual(field.defaultFactory, _factory)

    def test_bind(self):
        obj = object()
        field = self._makeOne()
        bound = field.bind(obj)
        self.assertEqual(bound.context, obj)
        expected = dict(field.__dict__)
        found = dict(bound.__dict__)
        found.pop('context')
        self.assertEqual(found, expected)
        self.assertEqual(bound.__class__, field.__class__)

    def test_validate_missing_not_required(self):
        missing = object()
        def _fail(value):
            return False
        field = self._makeOne(required=False,
                              missing_value=missing,
                              constraint=_fail,
                             )
        self.assertEqual(field.validate(missing), None) #doesn't raise

    def test_validate_missing_and_required(self):
        from zope.schema._bootstrapinterfaces import RequiredMissing
        missing = object()
        def _fail(value):
            return False
        field = self._makeOne(required=True,
                              missing_value=missing,
                              constraint=_fail,
                             )
        self.assertRaises(RequiredMissing, field.validate, missing)

    def test_validate_wrong_type(self):
        from zope.schema._bootstrapinterfaces import WrongType
        def _fail(value):
            return False
        field = self._makeOne(required=True,
                              constraint=_fail,
                             )
        field._type = str
        self.assertRaises(WrongType, field.validate, 1)

    def test_validate_constraint_fails(self):
        from zope.schema._bootstrapinterfaces import ConstraintNotSatisfied
        def _fail(value):
            return False
        field = self._makeOne(required=True,
                              constraint=_fail,
                             )
        field._type = int
        self.assertRaises(ConstraintNotSatisfied, field.validate, 1)

    def test_validate_constraint_raises_StopValidation(self):
        from zope.schema._bootstrapinterfaces import StopValidation
        def _fail(value):
            raise StopValidation
        field = self._makeOne(required=True,
                              constraint=_fail,
                             )
        field._type = int
        field.validate(1) #doesn't raise

    def test___eq___different_type(self):
        left = self._makeOne()
        class Derived(self._getTargetClass()):
            pass
        right = Derived()
        self.assertNotEqual(left, right)

    def test___eq___same_type_different_attrs(self):
        left = self._makeOne(required=True)
        right = self._makeOne(required=False)
        self.assertNotEqual(left, right)

    def test___eq___same_type_same_attrs(self):
        left = self._makeOne()
        right = self._makeOne()
        self.assertEqual(left, right)

    def test_get_miss(self):
        field = self._makeOne(__name__='nonesuch')
        inst = DummyInst()
        self.assertRaises(AttributeError, field.get, inst)

    def test_get_hit(self):
        field = self._makeOne(__name__='extant')
        inst = DummyInst()
        inst.extant = 'EXTANT'
        self.assertEqual(field.get(inst), 'EXTANT')

    def test_query_miss_no_default(self):
        field = self._makeOne(__name__='nonesuch')
        inst = DummyInst()
        self.assertEqual(field.query(inst), None)

    def test_query_miss_w_default(self):
        field = self._makeOne(__name__='nonesuch')
        inst = DummyInst()
        self.assertEqual(field.query(inst, 'DEFAULT'), 'DEFAULT')

    def test_query_hit(self):
        field = self._makeOne(__name__='extant')
        inst = DummyInst()
        inst.extant = 'EXTANT'
        self.assertEqual(field.query(inst), 'EXTANT')

    def test_set_readonly(self):
        field = self._makeOne(__name__='lirame', readonly=True)
        inst = DummyInst()
        self.assertRaises(TypeError, field.set, inst, 'VALUE')

    def test_set_hit(self):
        field = self._makeOne(__name__='extant')
        inst = DummyInst()
        inst.extant = 'BEFORE'
        field.set(inst, 'AFTER')
        self.assertEqual(inst.extant, 'AFTER')


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
        unittest.makeSuite(FieldTests),
    ))

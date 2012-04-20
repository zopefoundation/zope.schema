############################################################################## #
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
"""This set of tests exercises Object fields.
"""
import unittest

from zope.schema.tests.test_field import FieldTestBase
from zope.testing.cleanup import CleanUp


class ObjectTest(CleanUp, unittest.TestCase, FieldTestBase):
    """Test the Object Field."""

    def _getTargetClass(self):
        from zope.schema import Object
        return Object

    def _makeOne(self, *args, **kw):
        from zope.interface import Interface
        if 'schema' not in kw:
            kw['schema'] = Interface
        return super(ObjectTest, self)._makeOne(**kw)

    def _makeSchema(self):
        from zope.schema._compat import u
        from zope.interface import Attribute
        from zope.interface import Interface
        from zope.schema import TextLine
        from zope.schema._messageid import _

        class ITestSchema(Interface):
            """A test schema"""
            foo = TextLine(
                title=_("Foo"),
                description=_("Foo description"),
                default=u(""),
                required=True)
            bar = TextLine(
                title=_("Bar"),
                description=_("Bar description"),
                default=u(""),
                required=False)
            attribute = Attribute(
                "Test attribute, an attribute can't be validated.")

        return ITestSchema

    def getErrors(self, f, *args, **kw):
        from zope.schema.interfaces import WrongContainedType
        try:
            f(*args, **kw)
        except WrongContainedType as e:
            try:
                return e.args[0]
            except:
                return []
        self.fail('Expected WrongContainedType Error')

    def makeTestData(self):
        from zope.schema._compat import u
        from zope.interface import implementer
        schema = self._makeSchema()

        @implementer(schema)
        class TestClass(object):
            _foo = u('')
            _bar = u('')
            _attribute = u('')

            def getfoo(self):
                return self._foo
            def setfoo(self, value):
                self._foo = value
            foo = property(getfoo, setfoo, None, u('foo'))

            def getbar(self):
                return self._bar
            def setbar(self, value):
                self._bar = value
            bar = property(getbar, setbar, None, u('foo'))

            def getattribute(self):
                return self._attribute
            def setattribute(self, value):
                self._attribute = value
            attribute = property(getattribute, setattribute, None,
                                 u('attribute'))
        return TestClass()

    def makeFieldPropertyTestClass(self):
        from zope.interface import implementer
        from zope.schema.fieldproperty import FieldProperty
        schema = self._makeSchema()

        @implementer(schema)
        class FieldPropertyTestClass(object):
            foo = FieldProperty(schema['foo'])
            bar = FieldProperty(schema['bar'])
            attribute = FieldProperty(schema['attribute'])

        return FieldPropertyTestClass()

    def makeNotFullyImplementedTestData(self):
        from zope.interface import implementer
        from zope.schema.fieldproperty import FieldProperty
        schema = self._makeSchema()

        @implementer(schema)
        class NotFullyImplementedTestClass(object):
            foo = FieldProperty(schema['foo'])
            # bar = FieldProperty(schema['bar']): bar is not implemented
            # attribute

        return NotFullyImplementedTestClass()

    def invalidSchemas(self):
        return ['foo', 1, 0, {}, [], None]

    def validSchemas(self):
        from zope.interface import Interface
        return [Interface, self._makeSchema()]

    def test_init(self):
        from zope.schema.interfaces import ValidationError
        from zope.schema.interfaces import WrongType
        for schema in self.validSchemas():
            self._makeOne(schema=schema)
        for schema in self.invalidSchemas():
            self.assertRaises(ValidationError, self._makeOne, schema=schema)
            self.assertRaises(WrongType, self._makeOne, schema=schema)

    def testValidate(self):
        # this test of the base class is not applicable
        pass

    def testValidateRequired(self):
        # this test of the base class is not applicable
        pass

    def test_validate_required(self):
        from zope.schema._compat import u
        from zope.schema.interfaces import RequiredMissing
        field = self._makeOne(
            title=u('Required field'), description=u(''),
            readonly=False, required=True)
        self.assertRaises(RequiredMissing, field.validate, None)

    def test_validate_TestData(self):
        from zope.schema.interfaces import ValidationError
        from zope.schema.interfaces import RequiredMissing
        from zope.schema.interfaces import WrongContainedType
        schema = self._makeSchema()
        field = self._makeOne(schema=schema, required=False)
        data = self.makeTestData()
        field.validate(data)
        field = self._makeOne(schema=schema)
        field.validate(data)
        data.foo = None
        self.assertRaises(ValidationError, field.validate, data)
        self.assertRaises(WrongContainedType, field.validate, data)
        errors = self.getErrors(field.validate, data)
        self.assertEqual(errors[0], RequiredMissing('foo'))

    def test_validate_FieldPropertyTestData(self):
        from zope.schema.interfaces import ValidationError
        from zope.schema.interfaces import RequiredMissing
        schema = self._makeSchema()
        field = self._makeOne(schema=schema, required=False)
        data = self.makeFieldPropertyTestClass()
        field.validate(data)
        field = self._makeOne(schema=schema)
        field.validate(data)
        self.assertRaises(ValidationError, setattr, data, 'foo', None)
        self.assertRaises(RequiredMissing, setattr, data, 'foo', None)

    def test_validate_NotFullyImplementedTestData(self):
        from zope.schema.interfaces import SchemaNotFullyImplemented
        from zope.schema.interfaces import ValidationError
        from zope.schema.interfaces import WrongContainedType
        schema = self._makeSchema()
        field = self._makeOne(schema=schema, required=False)
        data = self.makeNotFullyImplementedTestData()
        self.assertRaises(ValidationError, field.validate, data)
        self.assertRaises(WrongContainedType, field.validate, data)
        errors = self.getErrors(field.validate, data)
        self.assertTrue(isinstance(errors[0], SchemaNotFullyImplemented))

    def test_validate_with_non_object_value(self):
        from zope.schema._compat import u
        from zope.interface import Interface
        from zope.interface import implementer
        from zope.schema import Object
        from zope.schema._messageid import _

        class ISchemaWithObjectFieldAsInterface(Interface):
            obj = Object(
                schema=Interface,
                title=_("Object"),
                description=_("object description"),
                required=False)

        @implementer(ISchemaWithObjectFieldAsInterface)
        class ClassWithObjectFieldAsInterface(object):

            _obj = None

            def getobj(self):
                return self._obj

            def setobj(self, value):
                self._obj = value

            obj = property(getobj, setobj, None, u('obj'))

        field = self._makeOne(
                    schema=ISchemaWithObjectFieldAsInterface,
                    required=False)
        instance = ClassWithObjectFieldAsInterface()
        instance.obj = (1, 1)
        field.validate(instance)

    def test_beforeAssignEvent(self):
        import zope.event
        from zope.schema.interfaces import IBeforeObjectAssignedEvent
        schema = self._makeSchema()
        field = self._makeOne(schema=schema, required=False,
                              __name__='object_field')
        data = self.makeTestData()
        events = []

        def register_event(event):
            events.append(event)
        zope.event.subscribers.append(register_event)

        class Dummy(object):
            pass
        context = Dummy()
        field.set(context, data)
        self.assertEqual(1, len(events))
        event = events[0]
        self.assertTrue(IBeforeObjectAssignedEvent.providedBy(event))
        self.assertEqual(data, event.object)
        self.assertEqual('object_field', event.name)
        self.assertEqual(context, event.context)

    # cycles
    def _makeCycles(self):
        from zope.interface import Interface
        from zope.interface import implementer
        from zope.schema import Object
        from zope.schema import List
        from zope.schema._messageid import _

        class IUnit(Interface):
            """A schema that participate to a cycle"""
            boss = Object(
                schema=Interface,
                title=_("Boss"),
                description=_("Boss description"),
                required=False,
                )
            members = List(
                value_type=Object(schema=Interface),
                title=_("Member List"),
                description=_("Member list description"),
                required=False,
                )

        class IPerson(Interface):
            """A schema that participate to a cycle"""
            unit = Object(
                schema=IUnit,
                title=_("Unit"),
                description=_("Unit description"),
                required=False,
                )

        IUnit['boss'].schema = IPerson
        IUnit['members'].value_type.schema = IPerson

        @implementer(IUnit)
        class Unit(object):
            def __init__(self, person, person_list):
                self.boss = person
                self.members = person_list

        @implementer(IPerson)
        class Person(object):
            def __init__(self, unit):
                self.unit = unit

        return IUnit, Person, Unit

    def test_with_cycles_validate(self):
        IUnit, Person, Unit = self._makeCycles()
        field = self._makeOne(schema=IUnit)
        person1 = Person(None)
        person2 = Person(None)
        unit = Unit(person1, [person1, person2])
        person1.unit = unit
        person2.unit = unit
        field.validate(unit)

    def test_with_cycles_object_not_valid(self):
        from zope.schema.interfaces import WrongContainedType
        IUnit, Person, Unit = self._makeCycles()
        field = self._makeOne(schema=IUnit)
        data = self.makeTestData()
        person1 = Person(None)
        person2 = Person(None)
        person3 = Person(data)
        unit = Unit(person3, [person1, person2])
        person1.unit = unit
        person2.unit = unit
        self.assertRaises(WrongContainedType, field.validate, unit)

    def test_with_cycles_collection_not_valid(self):
        from zope.schema.interfaces import WrongContainedType
        IUnit, Person, Unit = self._makeCycles()
        field = self._makeOne(schema=IUnit)
        data = self.makeTestData()
        person1 = Person(None)
        person2 = Person(None)
        person3 = Person(data)
        unit = Unit(person1, [person2, person3])
        person1.unit = unit
        person2.unit = unit
        self.assertRaises(WrongContainedType, field.validate, unit)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(ObjectTest),
    ))

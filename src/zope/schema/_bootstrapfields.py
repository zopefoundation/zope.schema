##############################################################################
#
# Copyright (c) 2002 Zope Foundation and Contributors.
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
"""Bootstrapping fields
"""
__docformat__ = 'restructuredtext'

import decimal
import fractions
import numbers
import threading
from math import isinf

from zope.interface import Attribute
from zope.interface import Invalid
from zope.interface import Interface
from zope.interface import providedBy
from zope.interface import implementer
from zope.interface.interfaces import IInterface
from zope.interface.interfaces import IMethod

from zope.event import notify

from zope.schema._bootstrapinterfaces import ConstraintNotSatisfied
from zope.schema._bootstrapinterfaces import IBeforeObjectAssignedEvent
from zope.schema._bootstrapinterfaces import IContextAwareDefaultFactory
from zope.schema._bootstrapinterfaces import IFromUnicode
from zope.schema._bootstrapinterfaces import IValidatable
from zope.schema._bootstrapinterfaces import NotAContainer
from zope.schema._bootstrapinterfaces import NotAnIterator
from zope.schema._bootstrapinterfaces import RequiredMissing
from zope.schema._bootstrapinterfaces import SchemaNotCorrectlyImplemented
from zope.schema._bootstrapinterfaces import SchemaNotFullyImplemented
from zope.schema._bootstrapinterfaces import SchemaNotProvided
from zope.schema._bootstrapinterfaces import StopValidation
from zope.schema._bootstrapinterfaces import TooBig
from zope.schema._bootstrapinterfaces import TooLong
from zope.schema._bootstrapinterfaces import TooShort
from zope.schema._bootstrapinterfaces import TooSmall
from zope.schema._bootstrapinterfaces import ValidationError
from zope.schema._bootstrapinterfaces import WrongType

from zope.schema._compat import text_type
from zope.schema._compat import integer_types

from zope.schema._schema import getFields


class _NotGiven(object):

    def __repr__(self): # pragma: no cover
        return "<Not Given>"


_NotGiven = _NotGiven()


class ValidatedProperty(object):

    def __init__(self, name, check=None, allow_none=False):
        self._name = name
        self._check = check
        self._allow_none = allow_none

    def __set__(self, inst, value):
        bypass_validation = (value is None and self._allow_none) or value == inst.missing_value
        if not bypass_validation:
            if self._check is not None:
                self._check(inst, value)
            else:
                inst.validate(value)
        inst.__dict__[self._name] = value

    def __get__(self, inst, owner):
        if inst is None:
            return self
        return inst.__dict__[self._name]


class DefaultProperty(ValidatedProperty):

    def __get__(self, inst, owner):
        if inst is None:
            return self
        defaultFactory = inst.__dict__.get('defaultFactory')
        # If there is no default factory, simply return the default.
        if defaultFactory is None:
            return inst.__dict__[self._name]
        # Get the default value by calling the factory. Some factories might
        # require a context to produce a value.
        if IContextAwareDefaultFactory.providedBy(defaultFactory):
            value = defaultFactory(inst.context)
        else:
            value = defaultFactory()
        # Check that the created value is valid.
        if self._check is not None:
            self._check(inst, value)
        elif value != inst.missing_value:
            inst.validate(value)
        return value


class Field(Attribute):

    # Type restrictions, if any
    _type = None
    context = None

    # If a field has no assigned value, it will be set to missing_value.
    missing_value = None

    # This is the default value for the missing_value argument to the
    # Field constructor.  A marker is helpful since we don't want to
    # overwrite missing_value if it is set differently on a Field
    # subclass and isn't specified via the constructor.
    __missing_value_marker = _NotGiven

    # Note that the "order" field has a dual existance:
    # 1. The class variable Field.order is used as a source for the
    #    monotonically increasing values used to provide...
    # 2. The instance variable self.order which provides a
    #    monotonically increasing value that tracks the creation order
    #    of Field (including Field subclass) instances.
    order = 0

    default = DefaultProperty('default')

    # These were declared as slots in zope.interface, we override them here to
    # get rid of the descriptors so they don't break .bind()
    __name__ = None
    interface = None
    _Element__tagged_values = None

    def __init__(self, title=u'', description=u'', __name__='',
                 required=True, readonly=False, constraint=None, default=None,
                 defaultFactory=None, missing_value=__missing_value_marker):
        """Pass in field values as keyword parameters.


        Generally, you want to pass either a title and description, or
        a doc string.  If you pass no doc string, it will be computed
        from the title and description.  If you pass a doc string that
        follows the Python coding style (title line separated from the
        body by a blank line), the title and description will be
        computed from the doc string.  Unfortunately, the doc string
        must be passed as a positional argument.

        Here are some examples:

        >>> from zope.schema._bootstrapfields import Field
        >>> f = Field()
        >>> f.__doc__, str(f.title), str(f.description)
        ('', '', '')

        >>> f = Field(title=u'sample')
        >>> str(f.__doc__), str(f.title), str(f.description)
        ('sample', 'sample', '')

        >>> f = Field(title=u'sample', description=u'blah blah\\nblah')
        >>> str(f.__doc__), str(f.title), str(f.description)
        ('sample\\n\\nblah blah\\nblah', 'sample', 'blah blah\\nblah')
        """
        __doc__ = ''
        if title:
            if description:
                __doc__ = "%s\n\n%s" % (title, description)
            else:
                __doc__ = title
        elif description:
            __doc__ = description

        super(Field, self).__init__(__name__, __doc__)
        self.title = title
        self.description = description
        self.required = required
        self.readonly = readonly
        if constraint is not None:
            self.constraint = constraint
        self.default = default
        self.defaultFactory = defaultFactory

        # Keep track of the order of field definitions
        Field.order += 1
        self.order = Field.order

        if missing_value is not self.__missing_value_marker:
            self.missing_value = missing_value

    def constraint(self, value):
        return True

    def bind(self, context):
        clone = self.__class__.__new__(self.__class__)
        clone.__dict__.update(self.__dict__)
        clone.context = context
        return clone

    def validate(self, value):
        if value == self.missing_value:
            if self.required:
                raise RequiredMissing(self.__name__).with_field_and_value(self, value)
        else:
            try:
                self._validate(value)
            except StopValidation:
                pass

    def __get_property_names_to_compare(self):
        # Return the set of property names to compare, ignoring
        # order
        names = {}  # used as set of property names, ignoring values
        for interface in providedBy(self):
            names.update(getFields(interface))

        # order will be different always, don't compare it
        names.pop('order', None)
        return names

    def __hash__(self):
        # Equal objects should have equal hashes;
        # equal hashes does not imply equal objects.
        value = (type(self), self.interface) + tuple(self.__get_property_names_to_compare())
        return hash(value)

    def __eq__(self, other):
        # should be the same type and in the same interface (or no interface at all)
        if self is other:
            return True

        if type(self) != type(other) or self.interface != other.interface:
            return False


        # should have the same properties
        names = self.__get_property_names_to_compare()
        # XXX: What about the property names of the other object? Even
        # though it's the same type, it could theoretically have
        # another interface that it `alsoProvides`.

        for name in names:
            if getattr(self, name) != getattr(other, name):
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def _validate(self, value):
        if self._type is not None and not isinstance(value, self._type):
            raise WrongType(value, self._type, self.__name__).with_field_and_value(self, value)

        if not self.constraint(value):
            raise ConstraintNotSatisfied(value, self.__name__).with_field_and_value(self, value)

    def get(self, object):
        return getattr(object, self.__name__)

    def query(self, object, default=None):
        return getattr(object, self.__name__, default)

    def set(self, object, value):
        if self.readonly:
            raise TypeError("Can't set values on read-only fields "
                            "(name=%s, class=%s.%s)"
                            % (self.__name__,
                               object.__class__.__module__,
                               object.__class__.__name__))
        setattr(object, self.__name__, value)


class Container(Field):

    def _validate(self, value):
        super(Container, self)._validate(value)

        if not hasattr(value, '__contains__'):
            try:
                iter(value)
            except TypeError:
                raise NotAContainer(value).with_field_and_value(self, value)


# XXX This class violates the Liskov Substituability Principle:  it
#     is derived from Container, but cannot be used everywhere an instance
#     of Container could be, because it's '_validate' is more restrictive.
class Iterable(Container):

    def _validate(self, value):
        super(Iterable, self)._validate(value)

        # See if we can get an iterator for it
        try:
            iter(value)
        except TypeError:
            raise NotAnIterator(value).with_field_and_value(self, value)


class Orderable(object):
    """Values of ordered fields can be sorted.

    They can be restricted to a range of values.

    Orderable is a mixin used in combination with Field.
    """

    min = ValidatedProperty('min', allow_none=True)
    max = ValidatedProperty('max', allow_none=True)

    def __init__(self, min=None, max=None, default=None, **kw):

        # Set min and max to None so that we can validate if
        # one of the super methods invoke validation.
        self.min = None
        self.max = None

        super(Orderable, self).__init__(**kw)

        # Now really set min and max
        self.min = min
        self.max = max

        # We've taken over setting default so it can be limited by min
        # and max.
        self.default = default

    def _validate(self, value):
        super(Orderable, self)._validate(value)

        if self.min is not None and value < self.min:
            raise TooSmall(value, self.min).with_field_and_value(self, value)

        if self.max is not None and value > self.max:
            raise TooBig(value, self.max).with_field_and_value(self, value)


class MinMaxLen(object):
    """Expresses constraints on the length of a field.

    MinMaxLen is a mixin used in combination with Field.
    """
    min_length = 0
    max_length = None

    def __init__(self, min_length=0, max_length=None, **kw):
        self.min_length = min_length
        self.max_length = max_length
        super(MinMaxLen, self).__init__(**kw)

    def _validate(self, value):
        super(MinMaxLen, self)._validate(value)

        if self.min_length is not None and len(value) < self.min_length:
            raise TooShort(value, self.min_length).with_field_and_value(self, value)

        if self.max_length is not None and len(value) > self.max_length:
            raise TooLong(value, self.max_length).with_field_and_value(self, value)


@implementer(IFromUnicode)
class Text(MinMaxLen, Field):
    """A field containing text used for human discourse."""
    _type = text_type

    def __init__(self, *args, **kw):
        super(Text, self).__init__(*args, **kw)

    def fromUnicode(self, str):
        """
        >>> from zope.schema.interfaces import WrongType
        >>> from zope.schema.interfaces import ConstraintNotSatisfied
        >>> from zope.schema import Text
        >>> from zope.schema._compat import text_type
        >>> t = Text(constraint=lambda v: 'x' in v)
        >>> t.fromUnicode(b"foo x spam") # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        zope.schema._bootstrapinterfaces.WrongType: ('foo x spam', <type 'unicode'>, '')
        >>> result = t.fromUnicode(u"foo x spam")
        >>> isinstance(result, bytes)
        False
        >>> str(result)
        'foo x spam'
        >>> t.fromUnicode(u"foo spam") # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        zope.schema._bootstrapinterfaces.ConstraintNotSatisfied: (u'foo spam', '')
        """
        self.validate(str)
        return str


class TextLine(Text):
    """A text field with no newlines."""

    def constraint(self, value):
        return '\n' not in value and '\r' not in value


class Password(TextLine):
    """A text field containing a text used as a password."""

    UNCHANGED_PASSWORD = object()

    def set(self, context, value):
        """Update the password.

        We use a special marker value that a widget can use
        to tell us that the password didn't change. This is
        needed to support edit forms that don't display the
        existing password and want to work together with
        encryption.

        """
        if value is self.UNCHANGED_PASSWORD:
            return
        super(Password, self).set(context, value)

    def validate(self, value):
        try:
            existing = bool(self.get(self.context))
        except AttributeError:
            existing = False
        if value is self.UNCHANGED_PASSWORD and existing:
            # Allow the UNCHANGED_PASSWORD value, if a password is set already
            return
        return super(Password, self).validate(value)


class Bool(Field):
    """A field representing a Bool."""

    _type = bool

    def _validate(self, value):
        # Convert integers to bools to they don't get mis-flagged
        # by the type check later.
        if isinstance(value, int):
            value = bool(value)
        Field._validate(self, value)

    def set(self, object, value):
        if isinstance(value, int):
            value = bool(value)
        Field.set(self, object, value)

    def fromUnicode(self, str):
        """
        >>> from zope.schema._bootstrapfields import Bool
        >>> from zope.schema.interfaces import IFromUnicode
        >>> b = Bool()
        >>> IFromUnicode.providedBy(b)
        True
        >>> b.fromUnicode('True')
        True
        >>> b.fromUnicode('')
        False
        >>> b.fromUnicode('true')
        True
        >>> b.fromUnicode('false') or b.fromUnicode('False')
        False
        """
        v = str == 'True' or str == 'true'
        self.validate(v)
        return v

class InvalidNumberLiteral(ValueError, ValidationError):
    """Invalid number literal."""

@implementer(IFromUnicode)
class Number(Orderable, Field):
    """
    A field representing a :class:`numbers.Number` and implementing
    :class:`zope.schema.interfaces.INumber`.

    The :meth:`fromUnicode` method will attempt to use the smallest or
    strictest possible type to represent incoming strings::

        >>> from zope.schema._bootstrapfields import Number
        >>> f = Number()
        >>> f.fromUnicode("1")
        1
        >>> f.fromUnicode("125.6")
        125.6
        >>> f.fromUnicode("1+0j")
        (1+0j)
        >>> f.fromUnicode("1/2")
        Fraction(1, 2)
        >>> f.fromUnicode(str(2**31234) + '.' + str(2**256)) # doctest: +ELLIPSIS
        Decimal('234...936')
        >>> f.fromUnicode("not a number") # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        InvalidNumberLiteral: Invalid literal for Decimal: 'not a number'

    .. versionadded:: 4.6.0
    """
    _type = numbers.Number

    # An ordered sequence of conversion routines. These should accept
    # a string and produce an object that is an instance of `_type`, or raise
    # a ValueError. The order should be most specific/strictest towards least
    # restrictive (in other words, lowest in the numeric tower towards highest).
    # We break this rule with fractions, though: a floating point number is
    # more generally useful and expected than a fraction, so we attempt to parse
    # as a float before a fraction.
    _unicode_converters = (int, float, fractions.Fraction, complex, decimal.Decimal)

    # The type of error we will raise if all conversions fail.
    _validation_error = InvalidNumberLiteral

    def fromUnicode(self, value):
        last_exc = None
        for converter in self._unicode_converters:
            try:
                val = converter(value)
                if converter is float and isinf(val) and decimal.Decimal in self._unicode_converters:
                    # Pass this on to decimal, if we're allowed
                    val = decimal.Decimal(value)
            except (ValueError, decimal.InvalidOperation) as e:
                last_exc = e
            else:
                self.validate(val)
                return val
        try:
            raise self._validation_error(*last_exc.args).with_field_and_value(self, value)
        finally:
            last_exc = None


class Complex(Number):
    """
    A field representing a :class:`numbers.Complex` and implementing
    :class:`zope.schema.interfaces.IComplex`.

    The :meth:`fromUnicode` method is like that for :class:`Number`,
    but doesn't allow Decimals::

        >>> from zope.schema._bootstrapfields import Complex
        >>> f = Complex()
        >>> f.fromUnicode("1")
        1
        >>> f.fromUnicode("125.6")
        125.6
        >>> f.fromUnicode("1+0j")
        (1+0j)
        >>> f.fromUnicode("1/2")
        Fraction(1, 2)
        >>> f.fromUnicode(str(2**31234) + '.' + str(2**256)) # doctest: +ELLIPSIS
        inf
        >>> f.fromUnicode("not a number") # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        InvalidNumberLiteral: Invalid literal for Decimal: 'not a number'

    .. versionadded:: 4.6.0
    """
    _type = numbers.Complex
    _unicode_converters = (int, float, complex, fractions.Fraction)


class Real(Complex):
    """
    A field representing a :class:`numbers.Real` and implementing
    :class:`zope.schema.interfaces.IReal`.

    The :meth:`fromUnicode` method is like that for :class:`Complex`,
    but doesn't allow Decimals or complex numbers::

        >>> from zope.schema._bootstrapfields import Real
        >>> f = Real()
        >>> f.fromUnicode("1")
        1
        >>> f.fromUnicode("125.6")
        125.6
        >>> f.fromUnicode("1+0j") # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        InvalidNumberLiteral: Invalid literal for Fraction: '1+0j'
        >>> f.fromUnicode("1/2")
        Fraction(1, 2)
        >>> f.fromUnicode(str(2**31234) + '.' + str(2**256)) # doctest: +ELLIPSIS
        inf
        >>> f.fromUnicode("not a number") # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        InvalidNumberLiteral: Invalid literal for Decimal: 'not a number'

    .. versionadded:: 4.6.0
    """
    _type = numbers.Real
    _unicode_converters = (int, float, fractions.Fraction)


class Rational(Real):
    """
    A field representing a :class:`numbers.Rational` and implementing
    :class:`zope.schema.interfaces.IRational`.

    The :meth:`fromUnicode` method is like that for :class:`Real`,
    but does not allow arbitrary floating point numbers::

        >>> from zope.schema._bootstrapfields import Rational
        >>> f = Rational()
        >>> f.fromUnicode("1")
        1
        >>> f.fromUnicode("1/2")
        Fraction(1, 2)
        >>> f.fromUnicode("125.6")
        Fraction(628, 5)
        >>> f.fromUnicode("1+0j") # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        InvalidNumberLiteral: Invalid literal for Fraction: '1+0j'
        >>> f.fromUnicode(str(2**31234) + '.' + str(2**256)) # doctest: +ELLIPSIS
        Fraction(777..., 330...)
        >>> f.fromUnicode("not a number") # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        InvalidNumberLiteral: Invalid literal for Decimal: 'not a number'

    .. versionadded:: 4.6.0
    """
    _type = numbers.Rational
    _unicode_converters = (int, fractions.Fraction)


class InvalidIntLiteral(ValueError, ValidationError):
    """Invalid int literal."""


class Integral(Rational):
    """
    A field representing a :class:`numbers.Integral` and implementing
    :class:`zope.schema.interfaces.IIntegral`.

    The :meth:`fromUnicode` method only allows integral values::

        >>> from zope.schema._bootstrapfields import Integral
        >>> f = Integral()
        >>> f.fromUnicode("125")
        125
        >>> f.fromUnicode("125.6") #doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        InvalidIntLiteral: invalid literal for int(): 125.6

    .. versionadded:: 4.6.0
    """
    _type = numbers.Integral
    _unicode_converters = (int,)
    _validation_error = InvalidIntLiteral


class Int(Integral):
    """A field representing a native integer type. and implementing
    :class:`zope.schema.interfaces.IInt`.
    """
    _type = integer_types
    _unicode_converters = (int,)


VALIDATED_VALUES = threading.local()

def _validate_fields(schema, value):
    errors = {}
    # Interface can be used as schema property for Object fields that plan to
    # hold values of any type.
    # Because Interface does not include any Attribute, it is obviously not
    # worth looping on its methods and filter them all out.
    if schema is Interface:
        return errors
    # if `value` is part of a cyclic graph, we need to break the cycle to avoid
    # infinite recursion. Collect validated objects in a thread local dict by
    # it's python represenation. A previous version was setting a volatile
    # attribute which didn't work with security proxy
    if id(value) in VALIDATED_VALUES.__dict__:
        return errors
    VALIDATED_VALUES.__dict__[id(value)] = True
    # (If we have gotten here, we know that `value` provides an interface
    # other than zope.interface.Interface;
    # iow, we can rely on the fact that it is an instance
    # that supports attribute assignment.)

    try:
        for name in schema.names(all=True):
            attribute = schema[name]
            if IMethod.providedBy(attribute):
                continue # pragma: no cover

            try:
                if IValidatable.providedBy(attribute):
                    # validate attributes that are fields
                    attribute.validate(getattr(value, name))
                # XXX: We're not even checking the existence of non-IField
                # Attribute objects.
            except ValidationError as error:
                errors[name] = error
            except AttributeError as error:
                # property for the given name is not implemented
                errors[name] = SchemaNotFullyImplemented(error).with_field_and_value(attribute, None)
    finally:
        del VALIDATED_VALUES.__dict__[id(value)]
    return errors


class _BoundSchema(object):
    """
    This class proxies a schema to get its fields bound to a context.
    """

    __slots__ = ('schema', 'context')

    def __new__(cls, schema, context):
        # Only proxy if we really need to.
        if schema is Interface or context is None:
            return schema
        return object.__new__(cls)

    def __init__(self, schema, context):
        self.schema = schema
        self.context = context

    def __getitem__(self, name):
        # Indexing this item will bind fields,
        # if possible
        attr = self.schema[name]
        try:
            return attr.bind(self.context)
        except AttributeError:
            return attr

    # but let all the rest slip to schema
    def __getattr__(self, name):
        return getattr(self.schema, name)


class Object(Field):
    """
    Implementation of :class:`zope.schema.interfaces.IObject`.
    """
    schema = None

    def __init__(self, schema=_NotGiven, **kw):
        """
        Object(schema=<Not Given>, *, validate_invariants=True, **kwargs)

        Create an `~.IObject` field. The keyword arguments are as for `~.Field`.

        .. versionchanged:: 4.6.0
           Add the keyword argument *validate_invariants*. When true (the default),
           the schema's ``validateInvariants`` method will be invoked to check
           the ``@invariant`` properties of the schema.
        .. versionchanged:: 4.6.0
           The *schema* argument can be ommitted in a subclass
           that specifies a ``schema`` attribute.
        """
        if schema is _NotGiven:
            schema = self.schema

        if not IInterface.providedBy(schema):
            raise WrongType

        self.schema = schema
        self.validate_invariants = kw.pop('validate_invariants', True)
        super(Object, self).__init__(**kw)

    def _validate(self, value):
        super(Object, self)._validate(value)

        # schema has to be provided by value
        if not self.schema.providedBy(value):
            raise SchemaNotProvided(self.schema, value).with_field_and_value(self, value)

        # check the value against schema
        schema_error_dict = _validate_fields(_BoundSchema(self.schema, value), value)
        invariant_errors = []
        if self.validate_invariants:
            try:
                self.schema.validateInvariants(value, invariant_errors)
            except Invalid:
                # validateInvariants raises a wrapper error around
                # all the errors it got if it got errors, in addition
                # to appending them to the errors list. We don't want
                # that, we raise our own error.
                pass

        if schema_error_dict or invariant_errors:
            errors = list(schema_error_dict.values()) + invariant_errors
            exception = SchemaNotCorrectlyImplemented(
                errors,
                self.__name__
            ).with_field_and_value(self, value)
            exception.schema_errors = schema_error_dict
            exception.invariant_errors = invariant_errors
            try:
                raise exception
            finally:
                # Break cycles
                del exception
                del invariant_errors
                del schema_error_dict
                del errors

    def set(self, object, value):
        # Announce that we're going to assign the value to the object.
        # Motivation: Widgets typically like to take care of policy-specific
        # actions, like establishing location.
        event = BeforeObjectAssignedEvent(value, self.__name__, object)
        notify(event)
        # The event subscribers are allowed to replace the object, thus we need
        # to replace our previous value.
        value = event.object
        super(Object, self).set(object, value)


@implementer(IBeforeObjectAssignedEvent)
class BeforeObjectAssignedEvent(object):
    """An object is going to be assigned to an attribute on another object."""

    def __init__(self, object, name, context):
        self.object = object
        self.name = name
        self.context = context

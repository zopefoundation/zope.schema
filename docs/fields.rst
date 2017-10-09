======
Fields
======

This document highlights unusual and subtle aspects of various fields and
field classes, and is not intended to be a general introduction to schema
fields.  Please see README.txt for a more general introduction.

While many field types, such as Int, TextLine, Text, and Bool are relatively
straightforward, a few have some subtlety.  We will explore the general
class of collections and discuss how to create a custom creation field; discuss
Choice fields, vocabularies, and their use with collections; and close with a
look at the standard zope.app approach to using these fields to find views
("widgets").

Scalars
-------

Scalar fields represent simple. immutable Python types.

Bytes
#####

:class:`zope.schema.Bytes` fields contain binary data, represented
as a sequence of bytes (``str`` in Python2, ``bytes`` in Python3).

Conversion from Unicode:

.. doctest::

   >>> from zope.schema import Bytes
   >>> obj = Bytes(constraint=lambda v: b'x' in v)
   >>> result = obj.fromUnicode(u" foo x.y.z bat")
   >>> isinstance(result, bytes)
   True
   >>> str(result.decode("ascii"))
   ' foo x.y.z bat'
   >>> obj.fromUnicode(u" foo y.z bat")
   Traceback (most recent call last):
   ...
   ConstraintNotSatisfied:  foo y.z bat

ASCII
#####

:class:`zope.schema.ASCII` fields are a restricted form of
:class:`zope.schema.Bytes`:  they can contain only 7-bit bytes.

Validation accepts empty strings:

.. doctest::

   >>> from zope.schema import ASCII
   >>> ascii = ASCII()
   >>> empty = ''
   >>> ascii._validate(empty)

and all kinds of alphanumeric strings:

.. doctest::

   >>> alphanumeric = "Bob\'s my 23rd uncle"
   >>> ascii._validate(alphanumeric)

but fails with 8-bit (encoded) strings:

.. doctest::

   >>> umlauts = "Köhlerstraße"
   >>> ascii._validate(umlauts)
   Traceback (most recent call last):
   ...
   InvalidValue

BytesLine
#########

:class:`zope.schema.BytesLine` fields are a restricted form of
:class:`zope.schema.Bytes`:  they cannot contain newlines.

ASCIILine
#########

:class:`zope.schema.BytesLine` fields are a restricted form of
:class:`zope.schema.ASCII`:  they cannot contain newlines.

Float
#####

:class:`zope.schema.Float` fields contain binary data, represented
as a a Python ``float``.

Conversion from Unicode:

.. doctest::

   >>> from zope.schema import Float
   >>> f = Float()
   >>> f.fromUnicode("1.25")
   1.25
   >>> f.fromUnicode("1.25.6") #doctest: +IGNORE_EXCEPTION_DETAIL
   Traceback (most recent call last):
   ...
   ValueError: invalid literal for float(): 1.25.6

Decimal
#######

:class:`zope.schema.Decimal` fields contain binary data, represented
as a a Python :class:`decimal.Decimal`.

Conversion from Unicode:

.. doctest::

   >>> from zope.schema import Decimal
   >>> f = Decimal()
   >>> import decimal
   >>> isinstance(f.fromUnicode("1.25"), decimal.Decimal)
   True
   >>> float(f.fromUnicode("1.25"))
   1.25
   >>> f.fromUnicode("1.25.6")
   Traceback (most recent call last):
   ...
   ValueError: invalid literal for Decimal(): 1.25.6

Datetime
########

:class:`zope.schema.Datetime` fields contain binary data, represented
as a a Python :class:`datetime.datetime`.

Date
####

:class:`zope.schema.Date` fields contain binary data, represented
as a a Python :class:`datetime.date`.

TimeDelta
#########

:class:`zope.schema.TimeDelta` fields contain binary data, represented
as a a Python :class:`datetime.timedelta`.

Time
####

:class:`zope.schema.Time` fields contain binary data, represented
as a a Python :class:`datetime.time`.

Choice
######

:class:`zope.schema.Choice` fields are constrained to values drawn
from a specified set, which can be static or dynamic.

Conversion from Unicode enforces the constraint:

.. doctest::

   >>> from zope.schema.interfaces import IFromUnicode
   >>> from zope.schema.vocabulary import SimpleVocabulary
   >>> from zope.schema import Choice
   >>> t = Choice(
   ...     vocabulary=SimpleVocabulary.fromValues([u'foo',u'bar']))
   >>> IFromUnicode.providedBy(t)
   True
   >>> t.fromUnicode(u"baz")
   Traceback (most recent call last):
   ...
   ConstraintNotSatisfied: baz
   >>> result = t.fromUnicode(u"foo")
   >>> isinstance(result, bytes)
   False
   >>> print(result)
   foo

By default, ValueErrors are thrown if duplicate values or tokens
are passed in. If you are using this vocabulary as part of a form
that is generated from non-pristine data, this may not be the
desired behavior. If you want to swallow these exceptions, pass
in swallow_duplicates=True when initializing the vocabulary. See
the test cases for an example.

URI
###

:class:`zope.schema.URI` fields contain native Python strings
(``str``), matching the "scheme:data" pattern.

Validation ensures that the pattern is matched:

.. doctest::

   >>> from zope.schema import URI
   >>> uri = URI(__name__='test')
   >>> uri.validate("http://www.python.org/foo/bar")
   >>> uri.validate("DAV:")
   >>> uri.validate("www.python.org/foo/bar")
   Traceback (most recent call last):
   ...
   InvalidURI: www.python.org/foo/bar

Conversion from Unicode:

.. doctest::

   >>> uri = URI(__name__='test')
   >>> uri.fromUnicode("http://www.python.org/foo/bar")
   'http://www.python.org/foo/bar'
   >>> uri.fromUnicode("          http://www.python.org/foo/bar")
   'http://www.python.org/foo/bar'
   >>> uri.fromUnicode("      \n    http://www.python.org/foo/bar\n")
   'http://www.python.org/foo/bar'
   >>> uri.fromUnicode("http://www.python.org/ foo/bar")
   Traceback (most recent call last):
   ...
   InvalidURI: http://www.python.org/ foo/bar

DottedName
##########

:class:`zope.schema.DottedName` fields contain native Python strings
(``str``), containing zero or more "dots" separating elements of the
name.  The minimum and maximum number of dots can be passed to the
constructor:

.. doctest::

   >>> from zope.schema import DottedName
   >>> DottedName(min_dots=-1)
   Traceback (most recent call last):
   ...
   ValueError: min_dots cannot be less than zero

   >>> DottedName(max_dots=-1)
   Traceback (most recent call last):
   ...
   ValueError: max_dots cannot be less than min_dots

   >>> DottedName(max_dots=1, min_dots=2)
   Traceback (most recent call last):
   ...
   ValueError: max_dots cannot be less than min_dots

   >>> dotted_name = DottedName(max_dots=1, min_dots=1)

   >>> from zope.interface.verify import verifyObject
   >>> from zope.schema.interfaces import IDottedName
   >>> verifyObject(IDottedName, dotted_name)
   True

   >>> dotted_name = DottedName(max_dots=1)
   >>> dotted_name.min_dots
   0

   >>> dotted_name = DottedName(min_dots=1)
   >>> dotted_name.max_dots
   >>> dotted_name.min_dots
   1

Validation ensures that the pattern is matched:

.. doctest::

   >>> dotted_name = DottedName(__name__='test')
   >>> dotted_name.validate("a.b.c")
   >>> dotted_name.validate("a")
   >>> dotted_name.validate("   a")
   Traceback (most recent call last):
   ...
   InvalidDottedName:    a

   >>> dotted_name = DottedName(__name__='test', min_dots=1)
   >>> dotted_name.validate('a.b')
   >>> dotted_name.validate('a.b.c.d')
   >>> dotted_name.validate('a')
   Traceback (most recent call last):
   ...
   InvalidDottedName: ('too few dots; 1 required', 'a')

   >>> dotted_name = DottedName(__name__='test', max_dots=0)
   >>> dotted_name.validate('a')
   >>> dotted_name.validate('a.b')
   Traceback (most recent call last):
   ...
   InvalidDottedName: ('too many dots; no more than 0 allowed', 'a.b')

   >>> dotted_name = DottedName(__name__='test', max_dots=2)
   >>> dotted_name.validate('a')
   >>> dotted_name.validate('a.b')
   >>> dotted_name.validate('a.b.c')
   >>> dotted_name.validate('a.b.c.d')
   Traceback (most recent call last):
   ...
   InvalidDottedName: ('too many dots; no more than 2 allowed', 'a.b.c.d')

   >>> dotted_name = DottedName(__name__='test', max_dots=1, min_dots=1)
   >>> dotted_name.validate('a.b')
   >>> dotted_name.validate('a')
   Traceback (most recent call last):
   ...
   InvalidDottedName: ('too few dots; 1 required', 'a')
   >>> dotted_name.validate('a.b.c')
   Traceback (most recent call last):
   ...
   InvalidDottedName: ('too many dots; no more than 1 allowed', 'a.b.c')

Id
##

:class:`zope.schema.Id` fields contain native Python strings
(``str``), matching either the URI pattern or a "dotted name".

Validation ensures that the pattern is matched:

.. doctest::

   >>> from zope.schema import Id
   >>> id = Id(__name__='test')
   >>> id.validate("http://www.python.org/foo/bar")
   >>> id.validate("zope.app.content")
   >>> id.validate("zope.app.content/a")
   Traceback (most recent call last):
   ...
   InvalidId: zope.app.content/a
   >>> id.validate("http://zope.app.content x y")
   Traceback (most recent call last):
   ...
   InvalidId: http://zope.app.content x y


Conversion from Unicode:

.. doctest::

   >>> id = Id(__name__='test')
   >>> id.fromUnicode("http://www.python.org/foo/bar")
   'http://www.python.org/foo/bar'
   >>> id.fromUnicode(u" http://www.python.org/foo/bar ")
   'http://www.python.org/foo/bar'
   >>> id.fromUnicode("http://www.python.org/ foo/bar")
   Traceback (most recent call last):
   ...
   InvalidId: http://www.python.org/ foo/bar
   >>> id.fromUnicode("      \n x.y.z \n")
   'x.y.z'


Collections
-----------

Normal fields typically describe the API of the attribute -- does it behave as a
Python Int, or a Float, or a Bool -- and various constraints to the model, such
as a maximum or minimum value.  Collection fields have additional requirements
because they contain other types, which may also be described and constrained.

For instance, imagine a list that contains non-negative floats and enforces
uniqueness. In a schema, this might be written as follows:

.. doctest::

   >>> from zope.interface import Interface
   >>> from zope.schema import List, Float
   >>> class IInventoryItem(Interface):
   ...     pricePoints = List(
   ...         title=u"Price Points",
   ...         unique=True,
   ...         value_type=Float(title=u"Price", min=0.0)
   ...     )

This indicates several things.

- pricePoints is an attribute of objects that implement IInventoryItem.
- The contents of pricePoints can be accessed and manipulated via a Python list
  API.
- Each member of pricePoints must be a non-negative float.
- Members cannot be duplicated within pricePoints: each must be must be unique.
- The attribute and its contents have descriptive titles.  Typically these
  would be message ids.

This declaration creates a field that implements a number of interfaces, among
them these:

.. doctest::

   >>> from zope.schema.interfaces import IList, ISequence, ICollection
   >>> IList.providedBy(IInventoryItem['pricePoints'])
   True
   >>> ISequence.providedBy(IInventoryItem['pricePoints'])
   True
   >>> ICollection.providedBy(IInventoryItem['pricePoints'])
   True

Creating a custom collection field
----------------------------------

Ideally, custom collection fields have interfaces that inherit appropriately
from either zope.schema.interfaces.ISequence or
zope.schema.interfaces.IUnorderedCollection.  Most collection fields should be
able to subclass :class:`zope.schema._field.AbstractCollection` to get the necessary
behavior.  Notice the behavior of the Set field in zope.schema: this
would also be necessary to implement a Bag.

Choices and Vocabularies
------------------------

Choice fields are the schema way of spelling enumerated fields and more.  By
providing a dynamically generated vocabulary, the choices available to a
choice field can be contextually calculated.

Simple choices do not have to explicitly use vocabularies:

.. doctest::

   >>> from zope.schema import Choice
   >>> f = Choice((640, 1028, 1600))
   >>> f.validate(640)
   >>> f.validate(960)
   Traceback (most recent call last):
   ...
   ConstraintNotSatisfied: 960
   >>> f.validate('bing')
   Traceback (most recent call last):
   ...
   ConstraintNotSatisfied: bing

More complex choices will want to use registered vocabularies.  Vocabularies
have a simple interface, as defined in
zope.schema.interfaces.IBaseVocabulary.  A vocabulary must minimally be able
to determine whether it contains a value, to create a term object for a value,
and to return a query interface (or None) to find items in itself.  Term
objects are an abstraction that wraps a vocabulary value.

The Zope application server typically needs a fuller interface that provides
"tokens" on its terms: ASCII values that have a one-to-one relationship to the
values when the vocabulary is asked to "getTermByToken".  If a vocabulary is
small, it can also support the IIterableVocabulary interface.

If a vocabulary has been registered, then the choice merely needs to pass the
vocabulary identifier to the "vocabulary" argument of the choice during
instantiation.

A start to a vocabulary implementation that may do all you need for many simple
tasks may be found in zope.schema.vocabulary.SimpleVocabulary.  Because
registered vocabularies are simply callables passed a context, many
registered vocabularies can simply be functions that rely on SimpleVocabulary:

.. doctest::

   >>> from zope.schema.vocabulary import SimpleVocabulary
   >>> def myDynamicVocabulary(context):
   ...     v = dynamic_context_calculation_that_returns_an_iterable(context)
   ...     return SimpleVocabulary.fromValues(v)
   ...

The vocabulary interface is simple enough that writing a custom vocabulary is
not too difficult itself.

See zope.schema.vocabulary.TreeVocabulary for another
IBaseVocabulary supporting vocabulary that provides a nested, tree-like
structure.

Choices and Collections
-----------------------

Choices are a field type and can be used as a value_type for collections. Just
as a collection of an "Int" value_type constrains members to integers, so a
choice-based value type constrains members to choices within the Choice's
vocabulary.  Typically in the Zope application server widgets are found not
only for the collection and the choice field but also for the vocabulary on
which the choice is based.

Using Choice and Collection Fields within a Widget Framework
------------------------------------------------------------

While fields support several use cases, including code documentation and data
description and even casting, a significant use case influencing their design is
to support form generation -- generating widgets for a field.  Choice and
collection fields are expected to be used within widget frameworks.  The
zope.app approach typically (but configurably) uses multiple dispatches to
find widgets on the basis of various aspects of the fields.

Widgets for all fields are found by looking up a browser view of the field
providing an input or display widget view.  Typically there is only a single
"widget" registered for Choice fields.  When it is looked up, it performs
another dispatch -- another lookup -- for a widget registered for both the field
and the vocabulary.  This widget typically has enough information to render
without a third dispatch.

Collection fields may fire several dispatches.  The first is the usual lookup
by field.  A single "widget" should be registered for ICollection, which does
a second lookup by field and value_type constraint, if any, or, theoretically,
if value_type is None, renders some absolutely generic collection widget that
allows input of any value imaginable: a check-in of such a widget would be
unexpected.  This second lookup may find a widget that knows how to render,
and stop.  However, the value_type may be a choice, which will usually fire a
third dispatch: a search for a browser widget for the collection field, the
value_type field, and the vocabulary.  Further lookups may even be configured
on the basis of uniqueness and other constraints.

This level of indirection may be unnecessary for some applications, and can be
disabled with simple ZCML changes within ``zope.app``.

=====
 API
=====

This document describes the low-level API of the interfaces and
classes provided by this package. The narrative documentation is a
better guide to the intended usage.

Interfaces
==========

.. autointerface:: zope.schema.interfaces.IField
.. autointerface:: zope.schema.interfaces.IChoice
.. autointerface:: zope.schema.interfaces.IContextAwareDefaultFactory
.. autointerface:: zope.schema.interfaces.IOrderable
.. autointerface:: zope.schema.interfaces.ILen
.. autointerface:: zope.schema.interfaces.IMinMax
.. autointerface:: zope.schema.interfaces.IMinMaxLen
.. autointerface:: zope.schema.interfaces.IInterfaceField
.. autointerface:: zope.schema.interfaces.IBool
.. autointerface:: zope.schema.interfaces.IObject


Conversions
-----------

.. autointerface:: zope.schema.interfaces.IFromBytes
.. autointerface:: zope.schema.interfaces.IFromUnicode


Strings
-------

.. autointerface:: zope.schema.interfaces.IBytes
.. autointerface:: zope.schema.interfaces.IBytesLine
.. autointerface:: zope.schema.interfaces.IText
.. autointerface:: zope.schema.interfaces.ITextLine
.. autointerface:: zope.schema.interfaces.IASCII
.. autointerface:: zope.schema.interfaces.IASCIILine
.. autointerface:: zope.schema.interfaces.INativeString
.. autointerface:: zope.schema.interfaces.INativeStringLine

.. autointerface:: zope.schema.interfaces.IPassword
.. autointerface:: zope.schema.interfaces.IURI
.. autointerface:: zope.schema.interfaces.IId
.. autointerface:: zope.schema.interfaces.IPythonIdentifier
.. autointerface:: zope.schema.interfaces.IDottedName


Numbers
-------

.. autointerface:: zope.schema.interfaces.INumber
.. autointerface:: zope.schema.interfaces.IComplex
.. autointerface:: zope.schema.interfaces.IReal
.. autointerface:: zope.schema.interfaces.IRational
.. autointerface:: zope.schema.interfaces.IIntegral

.. autointerface:: zope.schema.interfaces.IInt
.. autointerface:: zope.schema.interfaces.IFloat
.. autointerface:: zope.schema.interfaces.IDecimal

Date/Time
---------

.. autointerface:: zope.schema.interfaces.IDatetime
.. autointerface:: zope.schema.interfaces.IDate
.. autointerface:: zope.schema.interfaces.ITimedelta
.. autointerface:: zope.schema.interfaces.ITime


Collections
-----------
.. autointerface:: zope.schema.interfaces.IIterable
.. autointerface:: zope.schema.interfaces.IContainer
.. autointerface:: zope.schema.interfaces.ICollection
.. autointerface:: zope.schema.interfaces.ISequence
.. autointerface:: zope.schema.interfaces.IMutableSequence
.. autointerface:: zope.schema.interfaces.IUnorderedCollection
.. autointerface:: zope.schema.interfaces.IAbstractSet
.. autointerface:: zope.schema.interfaces.IAbstractBag

.. autointerface:: zope.schema.interfaces.ITuple
.. autointerface:: zope.schema.interfaces.IList
.. autointerface:: zope.schema.interfaces.ISet
.. autointerface:: zope.schema.interfaces.IFrozenSet

Mappings
~~~~~~~~
.. autointerface:: zope.schema.interfaces.IMapping
.. autointerface:: zope.schema.interfaces.IMutableMapping
.. autointerface:: zope.schema.interfaces.IDict


Events
------

.. autointerface:: zope.schema.interfaces.IBeforeObjectAssignedEvent
.. autointerface:: zope.schema.interfaces.IFieldEvent
.. autointerface:: zope.schema.interfaces.IFieldUpdatedEvent

Vocabularies
------------

.. autointerface:: zope.schema.interfaces.ITerm
.. autointerface:: zope.schema.interfaces.ITokenizedTerm
.. autointerface:: zope.schema.interfaces.ITitledTokenizedTerm
.. autointerface:: zope.schema.interfaces.ISource
.. autointerface:: zope.schema.interfaces.ISourceQueriables
.. autointerface:: zope.schema.interfaces.IContextSourceBinder
.. autointerface:: zope.schema.interfaces.IBaseVocabulary
.. autointerface:: zope.schema.interfaces.IIterableVocabulary
.. autointerface:: zope.schema.interfaces.IIterableSource
.. autointerface:: zope.schema.interfaces.IVocabulary
.. autointerface:: zope.schema.interfaces.IVocabularyTokenized
.. autointerface:: zope.schema.interfaces.ITreeVocabulary
.. autointerface:: zope.schema.interfaces.IVocabularyRegistry
.. autointerface:: zope.schema.interfaces.IVocabularyFactory

Exceptions
----------

.. autoexception:: zope.schema._bootstrapinterfaces.ValidationError

.. exception:: zope.schema.ValidationError

   The preferred alias for :class:`zope.schema._bootstrapinterfaces.ValidationError`.

.. autoexception:: zope.schema.interfaces.StopValidation
.. autoexception:: zope.schema.interfaces.RequiredMissing
.. autoexception:: zope.schema.interfaces.WrongType
.. autoexception:: zope.schema.interfaces.ConstraintNotSatisfied
.. autoexception:: zope.schema.interfaces.NotAContainer
.. autoexception:: zope.schema.interfaces.NotAnIterator
.. autoexception:: zope.schema.interfaces.NotAnInterface

Bounds
~~~~~~

.. autoexception:: zope.schema.interfaces.OutOfBounds
.. autoexception:: zope.schema.interfaces.OrderableOutOfBounds
.. autoexception:: zope.schema.interfaces.LenOutOfBounds
.. autoexception:: zope.schema.interfaces.TooSmall
.. autoexception:: zope.schema.interfaces.TooBig
.. autoexception:: zope.schema.interfaces.TooLong
.. autoexception:: zope.schema.interfaces.TooShort

.. autoexception:: zope.schema.interfaces.InvalidValue
.. autoexception:: zope.schema.interfaces.WrongContainedType
.. autoexception:: zope.schema.interfaces.NotUnique
.. autoexception:: zope.schema.interfaces.SchemaNotFullyImplemented
.. autoexception:: zope.schema.interfaces.SchemaNotProvided
.. autoexception:: zope.schema.interfaces.InvalidURI
.. autoexception:: zope.schema.interfaces.InvalidId
.. autoexception:: zope.schema.interfaces.InvalidDottedName
.. autoexception:: zope.schema.interfaces.Unbound

Schema APIs
===========

.. autofunction:: zope.schema.getFields
.. autofunction:: zope.schema.getFieldsInOrder
.. autofunction:: zope.schema.getFieldNames
.. autofunction:: zope.schema.getFieldNamesInOrder
.. autofunction:: zope.schema.getValidationErrors
   :noindex:
.. autofunction:: zope.schema.getSchemaValidationErrors
   :noindex:

Field Implementations
=====================

.. autoclass:: zope.schema.Field
.. autoclass:: zope.schema.Collection
.. autoclass:: zope.schema._field.AbstractCollection

.. autoclass:: zope.schema.Bool
   :no-show-inheritance:
.. autoclass:: zope.schema.Choice
   :no-show-inheritance:
.. autoclass:: zope.schema.Container
   :no-show-inheritance:
.. autoclass:: zope.schema.Date
   :no-show-inheritance:
.. autoclass:: zope.schema.Datetime
   :no-show-inheritance:
.. autoclass:: zope.schema.Dict

.. autoclass:: zope.schema.FrozenSet
   :no-show-inheritance:
.. autoclass:: zope.schema.Id
   :no-show-inheritance:
.. autoclass:: zope.schema.InterfaceField
   :no-show-inheritance:
.. autoclass:: zope.schema.Iterable
   :no-show-inheritance:
.. autoclass:: zope.schema.List
.. autoclass:: zope.schema.Mapping
   :no-show-inheritance:
.. autoclass:: zope.schema.MutableMapping
.. autoclass:: zope.schema.MutableSequence
.. autoclass:: zope.schema.MinMaxLen
.. autoclass:: zope.schema.Object
   :no-show-inheritance:
.. autoclass:: zope.schema.Orderable
.. autoclass:: zope.schema.Set
.. autoclass:: zope.schema.Sequence
.. autoclass:: zope.schema.Time
   :no-show-inheritance:
.. autoclass:: zope.schema.Timedelta
   :no-show-inheritance:
.. autoclass:: zope.schema.Tuple
.. autoclass:: zope.schema.URI
   :no-show-inheritance:

Strings
-------
.. autoclass:: zope.schema.ASCII
   :no-show-inheritance:
.. autoclass:: zope.schema.ASCIILine
   :no-show-inheritance:
.. autoclass:: zope.schema.Bytes
   :no-show-inheritance:
.. autoclass:: zope.schema.BytesLine
   :no-show-inheritance:
.. autoclass:: zope.schema.SourceText
   :no-show-inheritance:
.. autoclass:: zope.schema.Text
   :no-show-inheritance:
.. autoclass:: zope.schema.TextLine
   :no-show-inheritance:
.. autoclass:: zope.schema.NativeString
   :no-show-inheritance:
.. autoclass:: zope.schema.NativeStringLine
   :no-show-inheritance:
.. autoclass:: zope.schema.Password
   :no-show-inheritance:
.. autoclass:: zope.schema.DottedName
   :no-show-inheritance:
.. autoclass:: zope.schema.PythonIdentifier
   :no-show-inheritance:

Numbers
-------
.. autoclass:: zope.schema.Number
.. autoclass:: zope.schema.Complex
.. autoclass:: zope.schema.Real
.. autoclass:: zope.schema.Rational
.. autoclass:: zope.schema.Integral
.. autoclass:: zope.schema.Float
.. autoclass:: zope.schema.Int
.. autoclass:: zope.schema.Decimal

Vocabularies
============

.. automodule:: zope.schema.vocabulary

Accessors
=========

.. automodule:: zope.schema.accessors
.. autofunction:: zope.schema.accessors.accessors

=====
 API
=====

This document describes the low-level API of the interfaces and
classes provided by this package. The narrative documentation is a
better guide to the intended usage.

Interfaces
==========

.. autoclass:: zope.schema.interfaces.IField
.. autoclass:: zope.schema.interfaces.IFromUnicode
.. autoclass:: zope.schema.interfaces.IChoice
.. autoclass:: zope.schema.interfaces.IContextAwareDefaultFactory
.. autoclass:: zope.schema.interfaces.IOrderable
.. autoclass:: zope.schema.interfaces.ILen
.. autoclass:: zope.schema.interfaces.IMinMax
.. autoclass:: zope.schema.interfaces.IMinMaxLen
.. autoclass:: zope.schema.interfaces.IInterfaceField
.. autoclass:: zope.schema.interfaces.IBool
.. autoclass:: zope.schema.interfaces.IObject
.. autoclass:: zope.schema.interfaces.IDict

Strings
-------

.. autoclass:: zope.schema.interfaces.IBytes
.. autoclass:: zope.schema.interfaces.IBytesLine
.. autoclass:: zope.schema.interfaces.IText
.. autoclass:: zope.schema.interfaces.ITextLine
.. autoclass:: zope.schema.interfaces.IASCII
.. autoclass:: zope.schema.interfaces.IASCIILine

.. autoclass:: zope.schema.interfaces.IPassword
.. autoclass:: zope.schema.interfaces.IURI
.. autoclass:: zope.schema.interfaces.IId
.. autoclass:: zope.schema.interfaces.IDottedName


Numbers
-------

.. autoclass:: zope.schema.interfaces.IInt
.. autoclass:: zope.schema.interfaces.IFloat
.. autoclass:: zope.schema.interfaces.IDecimal

Date/Time
---------

.. autoclass:: zope.schema.interfaces.IDatetime
.. autoclass:: zope.schema.interfaces.IDate
.. autoclass:: zope.schema.interfaces.ITimedelta
.. autoclass:: zope.schema.interfaces.ITime


Collections
-----------
.. autoclass:: zope.schema.interfaces.IIterable
.. autoclass:: zope.schema.interfaces.IContainer
.. autoclass:: zope.schema.interfaces.ICollection
.. autoclass:: zope.schema.interfaces.ISequence
.. autoclass:: zope.schema.interfaces.IUnorderedCollection
.. autoclass:: zope.schema.interfaces.IAbstractSet
.. autoclass:: zope.schema.interfaces.IAbstractBag

.. autoclass:: zope.schema.interfaces.ITuple
.. autoclass:: zope.schema.interfaces.IList
.. autoclass:: zope.schema.interfaces.ISet
.. autoclass:: zope.schema.interfaces.IFrozenSet

Events
------

.. autoclass:: zope.schema.interfaces.IBeforeObjectAssignedEvent
.. autoclass:: zope.schema.interfaces.IFieldEvent
.. autoclass:: zope.schema.interfaces.IFieldUpdatedEvent

Vocabularies
------------

.. autoclass:: zope.schema.interfaces.ITerm
.. autoclass:: zope.schema.interfaces.ITokenizedTerm
.. autoclass:: zope.schema.interfaces.ITitledTokenizedTerm
.. autoclass:: zope.schema.interfaces.ISource
.. autoclass:: zope.schema.interfaces.ISourceQueriables
.. autoclass:: zope.schema.interfaces.IContextSourceBinder
.. autoclass:: zope.schema.interfaces.IBaseVocabulary
.. autoclass:: zope.schema.interfaces.IIterableVocabulary
.. autoclass:: zope.schema.interfaces.IIterableSource
.. autoclass:: zope.schema.interfaces.IVocabulary
.. autoclass:: zope.schema.interfaces.IVocabularyTokenized
.. autoclass:: zope.schema.interfaces.ITreeVocabulary
.. autoclass:: zope.schema.interfaces.IVocabularyRegistry
.. autoclass:: zope.schema.interfaces.IVocabularyFactory

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
.. autofunction:: zope.schema.getSchemaValidationErrors

Fields
======

.. autoclass:: zope.schema.Field
.. autoclass:: zope.schema._field.AbstractCollection
.. autoclass:: zope.schema.ASCII
   :no-show-inheritance:
.. autoclass:: zope.schema.ASCIILine
   :no-show-inheritance:
.. autoclass:: zope.schema.Bool
   :no-show-inheritance:
.. autoclass:: zope.schema.Bytes
   :no-show-inheritance:
.. autoclass:: zope.schema.BytesLine
   :no-show-inheritance:
.. autoclass:: zope.schema.Choice
   :no-show-inheritance:
.. autoclass:: zope.schema.Container
   :no-show-inheritance:
.. autoclass:: zope.schema.Date
   :no-show-inheritance:
.. autoclass:: zope.schema.Datetime
   :no-show-inheritance:
.. autoclass:: zope.schema.Decimal
   :no-show-inheritance:
.. autoclass:: zope.schema.Dict
   :no-show-inheritance:
.. autoclass:: zope.schema.DottedName
   :no-show-inheritance:

.. autoclass:: zope.schema.Float
   :no-show-inheritance:
.. autoclass:: zope.schema.FrozenSet
   :no-show-inheritance:
.. autoclass:: zope.schema.Id
   :no-show-inheritance:
.. autoclass:: zope.schema.Int
   :no-show-inheritance:
.. autoclass:: zope.schema.InterfaceField
   :no-show-inheritance:
.. autoclass:: zope.schema.Iterable
   :no-show-inheritance:
.. autoclass:: zope.schema.List
.. autoclass:: zope.schema.MinMaxLen
.. autoclass:: zope.schema.NativeString
.. autoclass:: zope.schema.NativeStringLine
.. autoclass:: zope.schema.Object
   :no-show-inheritance:
.. autoclass:: zope.schema.Orderable
.. autoclass:: zope.schema.Password
   :no-show-inheritance:
.. autoclass:: zope.schema.Set
.. autoclass:: zope.schema.SourceText
   :no-show-inheritance:
.. autoclass:: zope.schema.Text
   :no-show-inheritance:
.. autoclass:: zope.schema.TextLine
   :no-show-inheritance:
.. autoclass:: zope.schema.Time
   :no-show-inheritance:
.. autoclass:: zope.schema.Timedelta
   :no-show-inheritance:
.. autoclass:: zope.schema.Tuple
.. autoclass:: zope.schema.URI
   :no-show-inheritance:

Accessors
=========

.. automodule:: zope.schema.accessors
.. autofunction:: zope.schema.accessors.accessors

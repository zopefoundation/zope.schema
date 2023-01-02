=========
 Changes
=========

7.0.1 (2023-01-02)
==================

- Fix fallback when ``zope.i18nmessageid`` is not installed (regression
  introduced in 7.0.0).


7.0.0 (2023-01-01)
==================

- Add support for Python 3.11.

- Drop support for Python 2.7, 3.5, 3.6.

- Drop ``zope.schema._compat`` module.

- Fix test deprecation warning on Python 3.11.
  (`#112 <https://github.com/zopefoundation/zope.schema/issues/112>`_)

6.2.1 (2022-09-14)
==================

- Fix outsized integer test values that break tests on newer Python versions.
  (`#115 <https://github.com/zopefoundation/zope.schema/issues/115>`_)


6.2.0 (2021-10-18)
==================

- Add support for Python 3.10.


6.1.1 (2021-10-13)
==================

- Fix incompatibility introduced in 6.1.0:
  The `Bool` field constructor implicitly set required to False if not given.
  While this is the desired behavior in most common cases,
  it broke special cases.
  See `issue 104 <https://github.com/zopefoundation/zope.schema/issues/104>`_
  (scroll down, it is around the *reopen*).


6.1.0 (2021-02-09)
==================

- Fix ``IField.required`` to not be required by default.
  See `issue 104 <https://github.com/zopefoundation/zope.schema/issues/104>`_.

6.0.1 (2021-01-25)
==================

- Bring branch coverage to 100%.

- Add support for Python 3.9.

- Fix FieldUpdateEvent implementation by having an ``object`` attribute as the
  ``IFieldUpdatedEvent`` interfaces claims there should be.

6.0.0 (2020-03-21)
==================

- Require zope.interface 5.0.

- Ensure the resolution orders of all fields are consistent and make
  sense. In particular, ``Bool`` fields now correctly implement
  ``IBool`` before ``IFromUnicode``. See `issue 80
  <https://github.com/zopefoundation/zope.schema/issues/80>`_.

- Add support for Python 3.8.

- Drop support for Python 3.4.

5.0.1 (2020-03-06)
==================

- Fix: add ``Text.unicode_normalization = 'NFC'`` as default, because some are
  persisting schema fields. Setting that attribute only in ``__init__``
  breaks loading old objects.


5.0 (2020-03-06)
================

- Set ``IDecimal`` attributes ``min``, ``max`` and ``default`` as ``Decimal``
  type instead of ``Number``.
  See `issue 88 <https://github.com/zopefoundation/zope.schema/issues/88>`_.

- Enable unicode normalization for ``Text`` fields.
  The default is NFC normalization. Valid forms are 'NFC', 'NFKC', 'NFD', and
  'NFKD'. To disable normalization, set ``unicode_normalization`` to ``False``
  or ``None`` when calling ``__init__`` of the ``Text`` field.
  See `issue 86 <https://github.com/zopefoundation/zope.schema/issues/86>`_.


4.9.3 (2018-10-12)
==================

- Fix a ReST error in getDoc() results when having "subfields"
  with titles.


4.9.2 (2018-10-11)
==================

- Make sure that the title for ``IObject.validate_invariants`` is a unicode
  string.


4.9.1 (2018-10-05)
==================

- Fix ``SimpleTerm`` token for non-ASCII bytes values.


4.9.0 (2018-09-24)
==================

- Make ``NativeString`` and ``NativeStringLine`` distinct types that
  implement the newly-distinct interfaces ``INativeString`` and
  ``INativeStringLine``. Previously these were just aliases for either
  ``Text`` (on Python 3) or ``Bytes`` (on Python 2).

- Fix ``Field.getDoc()`` when ``value_type`` or ``key_type`` is
  present. Previously it could produce ReST that generated Sphinx
  warnings. See `issue 76 <https://github.com/zopefoundation/zope.schema/issues/76>`_.

- Make ``DottedName`` accept leading underscores for each segment.

- Add ``PythonIdentifier``, which accepts one segment of a dotted
  name, e.g., a python variable or class.

4.8.0 (2018-09-19)
==================

- Add the interface ``IFromBytes``, which is implemented by the
  numeric and bytes fields, as well as ``URI``, ``DottedName``, and
  ``Id``.

- Fix passing ``None`` as the description to a field constructor. See
  `issue 69 <https://github.com/zopefoundation/zope.schema/issues/69>`_.

4.7.0 (2018-09-11)
==================

- Make ``WrongType`` have an ``expected_type`` field.

- Add ``NotAnInterface``, an exception derived from ``WrongType`` and
  ``SchemaNotProvided`` and raised by the constructor of ``Object``
  and when validation fails for ``InterfaceField``.

- Give ``SchemaNotProvided`` a ``schema`` field.

- Give ``WrongContainedType`` an ``errors`` list.

- Give ``TooShort``, ``TooLong``, ``TooBig`` and ``TooSmall`` a
  ``bound`` field and the common superclasses ``LenOutOfBounds``,
  ``OrderableOutOfBounds``, respectively, both of which inherit from
  ``OutOfBounds``.

4.6.2 (2018-09-10)
==================

- Fix checking a field's constraint to set the ``field`` and ``value``
  properties if the constraint raises a ``ValidationError``. See
  `issue 66
  <https://github.com/zopefoundation/zope.schema/issues/66>`_.


4.6.1 (2018-09-10)
==================

- Fix the ``Field`` constructor to again allow ``MessageID`` values
  for the ``description``. This was a regression introduced with the
  fix for `issue 60
  <https://github.com/zopefoundation/zope.schema/issues/60>`_. See
  `issue 63
  <https://github.com/zopefoundation/zope.schema/issues/63>`_.


4.6.0 (2018-09-07)
==================

- Add support for Python 3.7.

- ``Object`` instances call their schema's ``validateInvariants``
  method by default to collect errors from functions decorated with
  ``@invariant`` when validating. This can be disabled by passing
  ``validate_invariants=False`` to the ``Object`` constructor. See
  `issue 10 <https://github.com/zopefoundation/zope.schema/issues/10>`_.

- ``ValidationError`` can be sorted on Python 3.

- ``DottedName`` and ``Id`` consistently handle non-ASCII unicode
  values on Python 2 and 3 by raising ``InvalidDottedName`` and
  ``InvalidId`` in ``fromUnicode`` respectively. Previously, a
  ``UnicodeEncodeError`` would be raised on Python 2 while Python 3
  would raise the descriptive exception.

- ``Field`` instances are hashable on Python 3, and use a defined
  hashing algorithm that matches what equality does on all versions of
  Python. Previously, on Python 2, fields were hashed based on their
  identity. This violated the rule that equal objects should have
  equal hashes, and now they do. Since having equal hashes does not
  imply that the objects are equal, this is not expected to be a
  compatibility problem. See `issue 36
  <https://github.com/zopefoundation/zope.schema/issues/36>`_.

- ``Field`` instances are only equal when their ``.interface`` is
  equal. In practice, this means that two otherwise identical fields
  of separate schemas are not equal, do not hash the same, and can
  both be members of the same ``dict`` or ``set``. Prior to this
  release, when hashing was identity based but only worked on Python
  2, that was the typical behaviour. (Field objects that are *not*
  members of a schema continue to compare and hash equal if they have
  the same attributes and interfaces.) See `issue 40
  <https://github.com/zopefoundation/zope.schema/issues/40>`_.

- Orderable fields, including ``Int``, ``Float``, ``Decimal``,
  ``Timedelta``, ``Date`` and ``Time``, can now have a
  ``missing_value`` without needing to specify concrete ``min`` and
  ``max`` values (they must still specify a ``default`` value). See
  `issue 9 <https://github.com/zopefoundation/zope.schema/issues/9>`_.

- ``Choice``, ``SimpleVocabulary`` and  ``SimpleTerm`` all gracefully
  handle using Unicode token values with non-ASCII characters by encoding
  them with the ``backslashreplace`` error handler. See `issue 15
  <https://github.com/zopefoundation/zope.schema/issues/15>`_ and `PR
  6 <https://github.com/zopefoundation/zope.schema/pull/6>`_.

- All instances of ``ValidationError`` have a ``field`` and ``value``
  attribute that is set to the field that raised the exception and the
  value that failed validation.

- ``Float``, ``Int`` and ``Decimal`` fields raise ``ValidationError``
  subclasses for literals that cannot be parsed. These subclasses also
  subclass ``ValueError`` for backwards compatibility.

- Add a new exception ``SchemaNotCorrectlyImplemented``, a subclass of
  ``WrongContainedType`` that is raised by the ``Object`` field. It
  has a dictionary (``schema_errors``) mapping invalid schema
  attributes to their corresponding exception, and a list
  (``invariant_errors``) containing the exceptions raised by
  validating invariants. See `issue 16
  <https://github.com/zopefoundation/zope.schema/issues/16>`_.

- Add new fields ``Mapping`` and ``MutableMapping``, corresponding to
  the collections ABCs of the same name; ``Dict`` now extends and
  specializes ``MutableMapping`` to only accept instances of ``dict``.

- Add new fields ``Sequence`` and ``MutableSequence``, corresponding
  to the collections ABCs of the same name; ``Tuple`` now extends
  ``Sequence`` and ``List`` now extends ``MutableSequence``.

- Add new field ``Collection``, implementing ``ICollection``. This is
  the base class of ``Sequence``. Previously this was known as
  ``AbstractCollection`` and was not public. It can be subclassed to
  add ``value_type``, ``_type`` and ``unique`` attributes at the class
  level, enabling a simpler constructor call. See `issue 23
  <https://github.com/zopefoundation/zope.schema/issues/23>`_.

- Make ``Object`` respect a ``schema`` attribute defined by a
  subclass, enabling a simpler constructor call. See `issue 23
  <https://github.com/zopefoundation/zope.schema/issues/23>`_.

- Add fields and interfaces representing Python's numeric tower. In
  descending order of generality these are ``Number``, ``Complex``,
  ``Real``, ``Rational`` and ``Integral``. The ``Int`` class extends
  ``Integral``, the ``Float`` class extends ``Real``, and the
  ``Decimal`` class extends ``Number``. See `issue 49
  <https://github.com/zopefoundation/zope.schema/issues/49>`_.

- Make ``Iterable`` and ``Container`` properly implement ``IIterable``
  and ``IContainer``, respectively.

- Make ``SimpleVocabulary.fromItems`` accept triples to allow
  specifying the title of terms. See `issue 18
  <https://github.com/zopefoundation/zope.schema/issues/18>`_.

- Make ``TreeVocabulary.fromDict`` only create
  ``ITitledTokenizedTerms`` when a title is actually provided.

- Make ``Choice`` fields reliably raise a ``ValidationError`` when a
  named vocabulary cannot be found; for backwards compatibility this
  is also a ``ValueError``. Previously this only worked when the
  default ``VocabularyRegistry`` was in use, not when it was replaced
  with `zope.vocabularyregistry
  <https://pypi.org/project/zope.vocabularyregistry/>`_. See `issue 55
  <https://github.com/zopefoundation/zope.schema/issues/55>`_.

- Make ``SimpleVocabulary`` and ``SimpleTerm`` have value-based
  equality and hashing methods.

- All fields of the schema of an ``Object`` field are bound to the
  top-level value being validated before attempting validation of
  their particular attribute. Previously only ``IChoice`` fields were
  bound. See `issue 17
  <https://github.com/zopefoundation/zope.schema/issues/17>`_.

- Share the internal logic of ``Object`` field validation and
  ``zope.schema.getValidationErrors``. See `issue 57
  <https://github.com/zopefoundation/zope.schema/issues/57>`_.


- Make ``Field.getDoc()`` return more information about the properties
  of the field, such as its required and readonly status. Subclasses
  can add more information using the new method
  ``Field.getExtraDocLines()``. This is used to generate Sphinx
  documentation when using `repoze.sphinx.autointerface
  <https://pypi.org/project/repoze.sphinx.autointerface/>`_. See
  `issue 60
  <https://github.com/zopefoundation/zope.schema/issues/60>`_.


4.5.0 (2017-07-10)
==================

- Drop support for Python 2.6, 3.2, and 3.3.

- Add support for Python 3.5 and 3.6.

- Drop support for 'setup.py test'. Use zope.testrunner instead.


4.4.2 (2014-09-04)
==================

- Fix description of min max field: max value is included, not excluded.


4.4.1 (2014-03-19)
==================

- Add support for Python 3.4.


4.4.0 (2014-01-22)
==================

- Add an event on field properties to notify that a field has been updated.
  This event enables definition of subscribers based on an event, a context
  and a field. The event contains also the old value and the new value.
  (also see package ``zope.schemaevent`` that define a field event handler)


4.3.3 (2014-01-06)
==================

- PEP 8 cleanup.

- Don't raise RequiredMissing if a field's defaultFactory returns the field's
  missing_value.

- Update ``boostrap.py`` to version 2.2.

- Add the ability to swallow ValueErrors when rendering a SimpleVocabulary,
  allowing for cases where vocabulary items may be duplicated (e.g., due to
  user input).

- Include the field name in ``ConstraintNotSatisfied``.


4.3.2 (2013-02-24)
==================

- Fix Python 2.6 support. (Forgot to run tox with all environments before last
  release.)


4.3.1 (2013-02-24)
==================

- Make sure that we do not fail during bytes decoding of term token when
  generated from a bytes value by ignoring all errors. (Another option would
  have been to hexlify the value, but that would break way too many tests.)


4.3.0 (2013-02-24)
==================

- Fix a bug where bytes values were turned into tokens inproperly in
  Python 3.

- Add ``zope.schema.fieldproperty.createFieldProperties()`` function which
  maps schema fields into ``FieldProperty`` instances.

4.2.2 (2012-11-21)
==================

- Add support for Python 3.3.

4.2.1 (2012-11-09)
==================

- Fix the default property of fields that have no defaultFactory attribute.


4.2.0 (2012-05-12)
==================

- Automate build of Sphinx HTML docs and running doctest snippets via tox.

- Drop explicit support for Python 3.1.

- Introduce NativeString and NativeStringLine which are equal to Bytes and
  BytesLine on Python 2 and Text and TextLine on Python 3.

- Change IURI from a Bytes string to a "native" string. This is a backwards
  incompatibility which only affects Python 3.

- Bring unit test coverage to 100%.

- Move doctests from the package and wired up as normal Sphinx documentation.

- Add explicit support for PyPy.

- Add support for continuous integration using ``tox`` and ``jenkins``.

- Drop the external ``six`` dependency in favor of a much-trimmed
  ``zope.schema._compat`` module.

- Ensure tests pass when run under ``nose``.

- Add ``setup.py dev`` alias (runs ``setup.py develop`` plus installs
  ``nose`` and ``coverage``).

- Add ``setup.py docs`` alias (installs ``Sphinx`` and dependencies).


4.1.1 (2012-03-23)
==================

- Remove trailing slash in MANIFEST.in, it causes Winbot to crash.


4.1.0 (2012-03-23)
==================

- Add TreeVocabulary for nested tree-like vocabularies.

- Fix broken Object field validation where the schema contains a Choice with
  ICountextSourceBinder source. In this case the vocabulary was not iterable
  because the field was not bound and the source binder didn't return the
  real vocabulary. Added simple test for IContextSourceBinder validation. But a
  test with an Object field with a schema using a Choice with
  IContextSourceBinder is still missing.

4.0.1 (2011-11-14)
==================

- Fix bug in ``fromUnicode`` method of ``DottedName`` which would fail
  validation on being given unicode. Introduced in 4.0.0.

4.0.0 (2011-11-09)
==================

- Fix deprecated unittest methods.

- Port to Python 3. This adds a dependency on six and removes support for
  Python 2.5.

3.8.1 (2011-09-23)
==================

- Fix broken Object field validation. Previous version was using a volatile
  property on object field values which ends in a ForbiddenAttribute error
  on security proxied objects.

3.8.0 (2011-03-18)
==================

- Implement a ``defaultFactory`` attribute for all fields. It is a callable
  that can be used to compute default values. The simplest case is::

    Date(defaultFactory=datetime.date.today)

  If the factory needs a context to compute a sensible default value, then it
  must provide ``IContextAwareDefaultFactory``, which can be used as follows::

    @provider(IContextAwareDefaultFactory)
    def today(context):
        return context.today()

    Date(defaultFactory=today)

3.7.1 (2010-12-25)
==================

- Rename the validation token, used in the validation of schema with Object
  Field to avoid infinite recursion:
  ``__schema_being_validated`` became ``_v_schema_being_validated``,
  a volatile attribute, to avoid persistency and therefore,
  read/write conflicts.

- Don't allow "[\]^`" in DottedName.
  https://bugs.launchpad.net/zope.schema/+bug/191236

3.7.0 (2010-09-12)
==================

- Improve error messages when term tokens or values are duplicates.

- Fix the buildout so the tests run.

3.6.4 (2010-06-08)
==================

- fix validation of schema with Object Field that specify Interface schema.

3.6.3 (2010-04-30)
==================

- Prefer the standard libraries doctest module to the one from zope.testing.

3.6.2 (2010-04-30)
==================

- Avoid maximum recursion when validating Object field that points to cycles

- Make the dependency on ``zope.i18nmessageid`` optional.

3.6.1 (2010-01-05)
==================

- Allow "setup.py test" to run at least a subset of the tests runnable
  via ``bin/test`` (227 for ``setup.py test`` vs. 258. for
  ``bin/test``)

- Make ``zope.schema._bootstrapfields.ValidatedProperty`` descriptor
  work under Jython.

- Make "setup.py test" tests pass on Jython.

3.6.0 (2009-12-22)
==================

- Prefer zope.testing.doctest over doctestunit.

- Extend validation error to hold the field name.

- Add FieldProperty class that uses Field.get and Field.set methods
  instead of storing directly on the instance __dict__.

3.5.4 (2009-03-25)
==================

- Don't fail trying to validate default value for Choice fields with
  IContextSourceBinder object given as a source. See
  https://bugs.launchpad.net/zope3/+bug/340416.

- Add an interface for ``DottedName`` field.

- Add ``vocabularyName`` attribute to the ``IChoice`` interface, change
  "vocabulary" attribute description to be more sensible, making it
  ``zope.schema.Field`` instead of plain ``zope.interface.Attribute``.

- Make IBool interface of Bool more important than IFromUnicode so adapters
  registered for IBool take precendence over adapters registered for
  IFromUnicode.


3.5.3 (2009-03-10)
==================

- Make Choice and Bool fields implement IFromUnicode interface, because
  they do provide the ``fromUnicode`` method.

- Change package's mailing list address to zope-dev at zope.org, as
  zope3-dev at zope.org is now retired.

- Fix package's documentation formatting. Change package's description.

- Add buildout part that builds Sphinx-generated documentation.

- Remove zpkg-related file.

3.5.2 (2009-02-04)
==================

- Made validation tests compatible with Python 2.5 again (hopefully not
  breaking Python 2.4)

- Add an __all__ package attribute to expose documentation.

3.5.1 (2009-01-31)
==================

- Stop using the old old set type.

- Make tests compatible and silent with Python 2.4.

- Fix __cmp__ method in ValidationError. Show some side effects based on the
  existing __cmp__ implementation. See validation.txt

- Make 'repr' of the ValidationError and its subclasses more sensible. This
  may require you to adapt your doctests for the new style, but now it makes
  much more sense for debugging for developers.

3.5.0a2 (2008-12-11)
====================

- Move zope.testing to "test" extras_require, as it is not needed
  for zope.schema itself.

- Change the order of classes in SET_TYPES tuple, introduced in
  previous release to one that was in 3.4 (SetType, set), because
  third-party code could be dependent on that order. The one
  example is z3c.form's converter.

3.5.0a1 (2008-10-10)
====================

- Add the doctests to the long description.

- Remove use of deprecated 'sets' module when running under Python 2.6.

- Remove spurious doctest failure when running under Python 2.6.

- Add support to bootstrap on Jython.

- Add helper methods for schema validation: ``getValidationErrors``
  and ``getSchemaValidationErrors``.

- zope.schema now works on Python2.5

3.4.0 (2007-09-28)
==================

Add BeforeObjectAssignedEvent that is triggered before the object
field sets a value.

3.3.0 (2007-03-15)
==================

Corresponds to the version of the zope.schema package shipped as part of
the Zope 3.3.0 release.

3.2.1 (2006-03-26)
==================

Corresponds to the version of the zope.schema package shipped as part of
the Zope 3.2.1 release.

Fix missing import of 'VocabularyRegistryError'.  See
http://www.zope.org/Collectors/Zope3-dev/544 .

3.2.0 (2006-01-05)
==================

Corresponds to the version of the zope.schema package shipped as part of
the Zope 3.2.0 release.

Add "iterable" sources to replace vocabularies, which are now deprecated
and scheduled for removal in Zope 3.3.

3.1.0 (2005-10-03)
==================

Corresponds to the version of the zope.schema package shipped as part of
the Zope 3.1.0 release.

Allow 'Choice' fields to take either a 'vocabulary' or a 'source'
argument (sources are a simpler implementation).

Add 'TimeDelta' and 'ASCIILine' field types.

3.0.0 (2004-11-07)
==================

Corresponds to the version of the zope.schema package shipped as part of
the Zope X3.0.0 release.

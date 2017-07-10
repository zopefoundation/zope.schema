Changes
=======

4.5.0 (unreleased)
------------------

- Drop support for Python 2.6, 3.2, and 3.3.

- Add support for Python 3.5 and 3.6.

- Drop support for 'setup.py test'. Use zope.testrunner instead.


4.4.2 (2014-09-04)
------------------

- Fix description of min max field: max value is included, not excluded.


4.4.1 (2014-03-19)
------------------

- Add support for Python 3.4.


4.4.0 (2014-01-22)
------------------

- Add an event on field properties to notify that a field has been updated.
  This event enables definition of subscribers based on an event, a context
  and a field. The event contains also the old value and the new value.
  (also see package ``zope.schemaevent`` that define a field event handler)


4.3.3 (2014-01-06)
------------------

- PEP 8 cleanup.

- Don't raise RequiredMissing if a field's defaultFactory returns the field's
  missing_value.

- Update ``boostrap.py`` to version 2.2.

- Add the ability to swallow ValueErrors when rendering a SimpleVocabulary,
  allowing for cases where vocabulary items may be duplicated (e.g., due to
  user input).

- Include the field name in ``ConstraintNotSatisfied``.


4.3.2 (2013-02-24)
------------------

- Fix Python 2.6 support. (Forgot to run tox with all environments before last
  release.)


4.3.1 (2013-02-24)
------------------

- Make sure that we do not fail during bytes decoding of term token when
  generated from a bytes value by ignoring all errors. (Another option would
  have been to hexlify the value, but that would break way too many tests.)


4.3.0 (2013-02-24)
------------------

- Fix a bug where bytes values were turned into tokens inproperly in
  Python 3.

- Add ``createFieldProperties()`` function which maps schema fields into
  ``FieldProperty`` instances.

4.2.2 (2012-11-21)
------------------

- Add support for Python 3.3.

4.2.1 (2012-11-09)
------------------

- Fix the default property of fields that have no defaultFactory attribute.


4.2.0 (2012-05-12)
------------------

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
------------------

- Remove trailing slash in MANIFEST.in, it causes Winbot to crash.


4.1.0 (2012-03-23)
------------------

- Add TreeVocabulary for nested tree-like vocabularies.

- Fix broken Object field validation where the schema contains a Choice with
  ICountextSourceBinder source. In this case the vocabulary was not iterable
  because the field was not bound and the source binder didn't return the
  real vocabulary. Added simple test for IContextSourceBinder validation. But a
  test with an Object field with a schema using a Choice with
  IContextSourceBinder is still missing.

4.0.1 (2011-11-14)
------------------

- Fix bug in ``fromUnicode`` method of ``DottedName`` which would fail
  validation on being given unicode. Introduced in 4.0.0.

4.0.0 (2011-11-09)
------------------

- Fix deprecated unittest methods.

- Port to Python 3. This adds a dependency on six and removes support for
  Python 2.5.

3.8.1 (2011-09-23)
------------------

- Fix broken Object field validation. Previous version was using a volatile
  property on object field values which ends in a ForbiddenAttribute error
  on security proxied objects.

3.8.0 (2011-03-18)
------------------

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
------------------

- Rename the validation token, used in the validation of schema with Object
  Field to avoid infinite recursion:
  ``__schema_being_validated`` became ``_v_schema_being_validated``,
  a volatile attribute, to avoid persistency and therefore,
  read/write conflicts.

- Don't allow "[\]^`" in DottedName.
  https://bugs.launchpad.net/zope.schema/+bug/191236

3.7.0 (2010-09-12)
------------------

- Improve error messages when term tokens or values are duplicates.

- Fix the buildout so the tests run.

3.6.4 (2010-06-08)
------------------

- fix validation of schema with Object Field that specify Interface schema.

3.6.3 (2010-04-30)
------------------

- Prefer the standard libraries doctest module to the one from zope.testing.

3.6.2 (2010-04-30)
------------------

- Avoid maximum recursion when validating Object field that points to cycles

- Make the dependency on ``zope.i18nmessageid`` optional.

3.6.1 (2010-01-05)
------------------

- Allow "setup.py test" to run at least a subset of the tests runnable
  via ``bin/test`` (227 for ``setup.py test`` vs. 258. for
  ``bin/test``)

- Make ``zope.schema._bootstrapfields.ValidatedProperty`` descriptor
  work under Jython.

- Make "setup.py test" tests pass on Jython.

3.6.0 (2009-12-22)
------------------

- Prefer zope.testing.doctest over doctestunit.

- Extend validation error to hold the field name.

- Add FieldProperty class that uses Field.get and Field.set methods
  instead of storing directly on the instance __dict__.

3.5.4 (2009-03-25)
------------------

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
------------------

- Make Choice and Bool fields implement IFromUnicode interface, because
  they do provide the ``fromUnicode`` method.

- Change package's mailing list address to zope-dev at zope.org, as
  zope3-dev at zope.org is now retired.

- Fix package's documentation formatting. Change package's description.

- Add buildout part that builds Sphinx-generated documentation.

- Remove zpkg-related file.

3.5.2 (2009-02-04)
------------------

- Made validation tests compatible with Python 2.5 again (hopefully not
  breaking Python 2.4)

- Add an __all__ package attribute to expose documentation.

3.5.1 (2009-01-31)
------------------

- Stop using the old old set type.

- Make tests compatible and silent with Python 2.4.

- Fix __cmp__ method in ValidationError. Show some side effects based on the
  existing __cmp__ implementation. See validation.txt

- Make 'repr' of the ValidationError and its subclasses more sensible. This
  may require you to adapt your doctests for the new style, but now it makes
  much more sense for debugging for developers.

3.5.0a2 (2008-12-11)
--------------------

- Move zope.testing to "test" extras_require, as it is not needed
  for zope.schema itself.

- Change the order of classes in SET_TYPES tuple, introduced in
  previous release to one that was in 3.4 (SetType, set), because
  third-party code could be dependent on that order. The one
  example is z3c.form's converter.

3.5.0a1 (2008-10-10)
--------------------

- Add the doctests to the long description.

- Remove use of deprecated 'sets' module when running under Python 2.6.

- Remove spurious doctest failure when running under Python 2.6.

- Add support to bootstrap on Jython.

- Add helper methods for schema validation: ``getValidationErrors``
  and ``getSchemaValidationErrors``.

- zope.schema now works on Python2.5

3.4.0 (2007-09-28)
------------------

Add BeforeObjectAssignedEvent that is triggered before the object
field sets a value.

3.3.0 (2007-03-15)
------------------

Corresponds to the version of the zope.schema package shipped as part of
the Zope 3.3.0 release.

3.2.1 (2006-03-26)
------------------

Corresponds to the version of the zope.schema package shipped as part of
the Zope 3.2.1 release.

Fix missing import of 'VocabularyRegistryError'.  See
http://www.zope.org/Collectors/Zope3-dev/544 .

3.2.0 (2006-01-05)
------------------

Corresponds to the version of the zope.schema package shipped as part of
the Zope 3.2.0 release.

Add "iterable" sources to replace vocabularies, which are now deprecated
and scheduled for removal in Zope 3.3.

3.1.0 (2005-10-03)
------------------

Corresponds to the version of the zope.schema package shipped as part of
the Zope 3.1.0 release.

Allow 'Choice' fields to take either a 'vocabulary' or a 'source'
argument (sources are a simpler implementation).

Add 'TimeDelta' and 'ASCIILine' field types.

3.0.0 (2004-11-07)
------------------

Corresponds to the version of the zope.schema package shipped as part of
the Zope X3.0.0 release.

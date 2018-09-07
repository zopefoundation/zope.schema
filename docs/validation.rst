=================
Schema Validation
=================

There are two helper methods to verify schemas and interfaces:

.. autofunction:: zope.schema.getValidationErrors
.. autofunction:: zope.schema.getSchemaValidationErrors

Invariants are `documented by zope.interface
<https://zopeinterface.readthedocs.io/en/latest/README.html#invariants>`_.

Create an interface to validate against:

.. doctest::

   >>> import zope.interface
   >>> import zope.schema
   >>> _a_greater_b_called = []
   >>> class ITwoInts(zope.interface.Interface):
   ...     a = zope.schema.Int(max=10)
   ...     b = zope.schema.Int(min=5)
   ...
   ...     @zope.interface.invariant
   ...     def a_greater_b(obj):
   ...         _a_greater_b_called.append(obj)
   ...         if obj.a <= obj.b:
   ...             raise zope.interface.Invalid("%s<=%s" % (obj.a, obj.b))
   ...

Create a silly model:

.. doctest::

   >>> class TwoInts(object):
   ...     pass

Create an instance of TwoInts but do not set attributes. We get two errors:

.. doctest::

   >>> ti = TwoInts()
   >>> r = zope.schema.getValidationErrors(ITwoInts, ti)
   >>> r.sort()
   >>> len(r)
   2
   >>> r[0][0]
   'a'
   >>> r[0][1].__class__.__name__
   'SchemaNotFullyImplemented'
   >>> r[0][1].args[0].args
   ("'TwoInts' object has no attribute 'a'",)
   >>> r[1][0]
   'b'
   >>> r[1][1].__class__.__name__
   'SchemaNotFullyImplemented'
   >>> r[1][1].args[0].args
   ("'TwoInts' object has no attribute 'b'",)

The `getSchemaValidationErrors` function returns the same result:

.. doctest::

   >>> r = zope.schema.getSchemaValidationErrors(ITwoInts, ti)
   >>> r.sort()
   >>> len(r)
   2
   >>> r[0][0]
   'a'
   >>> r[0][1].__class__.__name__
   'SchemaNotFullyImplemented'
   >>> r[0][1].args[0].args
   ("'TwoInts' object has no attribute 'a'",)
   >>> r[1][0]
   'b'
   >>> r[1][1].__class__.__name__
   'SchemaNotFullyImplemented'
   >>> r[1][1].args[0].args
   ("'TwoInts' object has no attribute 'b'",)

Note that see no error from the invariant because the invariants are not
validated if there are other schema errors.

When we set a valid value for `a` we still get the same error for `b`:

.. doctest::

   >>> ti.a = 11
   >>> errors = zope.schema.getValidationErrors(ITwoInts, ti)
   >>> errors.sort()
   >>> len(errors)
   2
   >>> errors[0][0]
   'a'
   >>> print(errors[0][1].doc())
   Value is too big
   >>> errors[0][1].__class__.__name__
   'TooBig'
   >>> errors[0][1].args
   (11, 10)
   >>> errors[1][0]
   'b'
   >>> errors[1][1].__class__.__name__
   'SchemaNotFullyImplemented'
   >>> errors[1][1].args[0].args
   ("'TwoInts' object has no attribute 'b'",)


After setting a valid value for `a` there is only the error for the missing `b`
left:

.. doctest::

   >>> ti.a = 8
   >>> r = zope.schema.getValidationErrors(ITwoInts, ti)
   >>> r
   [('b', SchemaNotFullyImplemented(...AttributeError...))]
   >>> r[0][1].args[0].args
   ("'TwoInts' object has no attribute 'b'",)


After setting valid value for `b` the schema is valid so the invariants are
checked. As `b>a` the invariant fails:

.. doctest::

   >>> ti.b = 10
   >>> errors = zope.schema.getValidationErrors(ITwoInts, ti)
   >>> len(errors)
   1
   >>> errors[0][0] is None
   True
   >>> errors[0][1].__class__.__name__
   'Invalid'
   >>> len(_a_greater_b_called)
   1


When using `getSchemaValidationErrors` we do not get an error any more:

.. doctest::

   >>> zope.schema.getSchemaValidationErrors(ITwoInts, ti)
   []


Set `b=5` so everything is fine:

.. doctest::

   >>> ti.b = 5
   >>> del _a_greater_b_called[:]
   >>> zope.schema.getValidationErrors(ITwoInts, ti)
   []
   >>> len(_a_greater_b_called)
   1


Compare ValidationError
-----------------------

There was an issue with compare validation error with something else then an
exceptions. Let's test if we can compare ValidationErrors with different things

.. doctest::

   >>> from zope.schema._bootstrapinterfaces import ValidationError
   >>> v1 = ValidationError('one')
   >>> v2 = ValidationError('one')
   >>> v3 = ValidationError('another one')

A ValidationError with the same arguments compares:

.. doctest::

   >>> v1 == v2
   True

but not with an error with different arguments:

.. doctest::

   >>> v1 == v3
   False

We can also compare validation errors with other things then errors. This
was running into an AttributeError in previous versions of zope.schema. e.g.
AttributeError: 'NoneType' object has no attribute 'args'

.. doctest::

   >>> v1 == None
   False
   >>> v1 == object()
   False
   >>> v1 == False
   False
   >>> v1 == True
   False
   >>> v1 == 0
   False
   >>> v1 == 1
   False
   >>> v1 == int
   False

If we compare a ValidationError with another validation error based class,
we will get the following result:

.. doctest::

   >>> from zope.schema._bootstrapinterfaces import RequiredMissing
   >>> r1 = RequiredMissing('one')
   >>> v1 == r1
   True

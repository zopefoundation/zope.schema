***********
zope.schema
***********

Schemas extend the notion of interfaces to detailed descriptions of
Attributes (but not methods).  Every schema is an interface and
specifies the public fields of an object.  A *field* roughly
corresponds to an attribute of a python object.  But a Field provides
space for at least a title and a description.  It can also constrain
its value and provide a validation method.  Besides you can optionally
specify characteristics such as its value being read-only or not
required.

See 'src/zope/schema/README.txt' for more information.

Releases
********

==================
3.3.0 (2007/03/15)
==================

Corresponds to the version of the zope.schema package shipped as part of
the Zope 3.3.0 release.

==================
3.2.1 (2006/03/26)
==================

Corresponds to the version of the zope.schema package shipped as part of
the Zope 3.2.1 release.

Fixed missing import of 'VocabularyRegistryError'.  See
http://www.zope.org/Collectors/Zope3-dev/544 .

==================
3.2.0 (2006/01/05)
==================

Corresponds to the version of the zope.schema package shipped as part of
the Zope 3.2.0 release.

Added "iterable" sources to replace vocabularies, which are now deprecated
and scheduled for removal in Zope 3.3.

==================
3.1.0 (2005/10/03)
==================

Corresponds to the version of the zope.schema package shipped as part of
the Zope 3.1.0 release.

Allowed 'Choice' fields to take either a 'vocabulary' or a 'source'
argument (sources are a simpler implementation).

Added 'TimeDelta' and 'ASCIILine' field types.

==================
3.0.0 (2004/11/07)
==================

Corresponds to the version of the zope.schema package shipped as part of
the Zope X3.0.0 release.

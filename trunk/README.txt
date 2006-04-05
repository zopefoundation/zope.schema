zope.schema Package Readme
==========================

Overview
--------

Schemas extend the notion of interfaces to detailed descriptions of Attributes
(but not methods). Every schema is an interface and specifies the public
fields of an object. A *field* roughly corresponds to an attribute of a
python object. But a Field provides space for at least a title and a
description. It can also constrain its value and provide a validation method.
Besides you can optionally specify characteristics such as its value being
read-only or not required.

See 'src/zope/schema/README.txt' for more information.

Changes
-------

See CHANGES.txt.

Installation
------------

See INSTALL.txt.


Developer Resources
-------------------

- Subversion browser:

  http://svn.zope.org/zope.schema/

- Read-only Subversion checkout:

  $ svn co svn://svn.zope.org/repos/main/zope.schema/trunk

- Writable Subversion checkout:

  $ svn co svn://svn.zope.org/repos/main/zope.schema/trunk

- Note that the 'src/zope/schema' package is acutally a 'svn:externals' link
  to the corresponding package in the Zope3 trunk (or to a specific tag,
  for released versions of the package).

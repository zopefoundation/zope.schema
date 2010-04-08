##############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors.
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
"""Setup for zope.schema package

$Id$
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(name='zope.schema',
      version = '3.4.1dev',
      url='http://pypi.python.org/pypi/zope.schema',
      license='ZPL 2.1',
      description='Zope3 Data Schemas',
      author='Zope Foundation and Contributors',
      author_email='zope3-dev@zope.org',
      long_description=(read('src', 'zope', 'schema', 'README.txt')
                        + '\n\n' +
                        read('CHANGES.txt')),

      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['zope',],
      install_requires=['setuptools',
                        'zope.i18nmessageid',
                        'zope.interface',
                        'zope.event',
                        # testing dependencies
                        'zope.testing',
                       ],
      include_package_data = True,
      zip_safe = False,
      )

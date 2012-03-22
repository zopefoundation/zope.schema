##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
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
"""Test of the Vocabulary and related support APIs.
"""
import unittest

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from zope.interface.verify import verifyObject
from zope.interface.exceptions import DoesNotImplement
from zope.interface import Interface, implementer
from zope.interface.common.mapping import IEnumerableMapping

from zope.schema import interfaces
from zope.schema import vocabulary


class DummyRegistry(vocabulary.VocabularyRegistry):
    def get(self, object, name):
        v = SampleVocabulary()
        v.object = object
        v.name = name
        return v


class BaseTest(unittest.TestCase):
    # Clear the vocabulary and presentation registries on each side of
    # each test.

    def setUp(self):
        vocabulary._clear()

    def tearDown(self):
        vocabulary._clear()


class RegistryTests(BaseTest):
    """Tests of the simple vocabulary and presentation registries."""

    def test_setVocabularyRegistry(self):
        r = DummyRegistry()
        vocabulary.setVocabularyRegistry(r)
        self.assertTrue(vocabulary.getVocabularyRegistry() is r)

    def test_getVocabularyRegistry(self):
        r = vocabulary.getVocabularyRegistry()
        self.assertTrue(interfaces.IVocabularyRegistry.providedBy(r))

    # TODO: still need to test the default implementation

class SampleTerm(object):
    pass

@implementer(interfaces.IVocabulary)
class SampleVocabulary(object):

    def __iter__(self):
        return iter([self.getTerm(x) for x in range(0, 10)])

    def __contains__(self, value):
        return 0 <= value < 10

    def __len__(self):
        return 10

    def getTerm(self, value):
        if value in self:
            t = SampleTerm()
            t.value = value
            t.double = 2 * value
            return t
        raise LookupError("no such value: %r" % value)


class SimpleVocabularyTests(unittest.TestCase):

    list_vocab = vocabulary.SimpleVocabulary.fromValues([1, 2, 3])
    items_vocab = vocabulary.SimpleVocabulary.fromItems(
        [('one', 1), ('two', 2), ('three', 3), ('fore!', 4)])

    def test_simple_term(self):
        t = vocabulary.SimpleTerm(1)
        verifyObject(interfaces.ITokenizedTerm, t)
        self.assertEqual(t.value, 1)
        self.assertEqual(t.token, "1")
        t = vocabulary.SimpleTerm(1, "One")
        verifyObject(interfaces.ITokenizedTerm, t)
        self.assertEqual(t.value, 1)
        self.assertEqual(t.token, "One")

    def test_simple_term_title(self):
        t = vocabulary.SimpleTerm(1)
        verifyObject(interfaces.ITokenizedTerm, t)
        self.assertRaises(DoesNotImplement, verifyObject,
            interfaces.ITitledTokenizedTerm, t)
        self.assertTrue(t.title is None)
        t = vocabulary.SimpleTerm(1, title="Title")
        verifyObject(interfaces.ITokenizedTerm, t)
        verifyObject(interfaces.ITitledTokenizedTerm, t)
        self.assertEqual(t.title, "Title")

    def test_order(self):
        value = 1
        for t in self.list_vocab:
            self.assertEqual(t.value, value)
            value += 1

        value = 1
        for t in self.items_vocab:
            self.assertEqual(t.value, value)
            value += 1

    def test_implementation(self):
        self.assertTrue(verifyObject(interfaces.IVocabulary, self.list_vocab))
        self.assertTrue(
            verifyObject(interfaces.IVocabularyTokenized, self.list_vocab))
        self.assertTrue(verifyObject(interfaces.IVocabulary, self.items_vocab))
        self.assertTrue(
            verifyObject(interfaces.IVocabularyTokenized, self.items_vocab))

    def test_addt_interfaces(self):
        class IStupid(Interface):
            pass
        v = vocabulary.SimpleVocabulary.fromValues([1, 2, 3], IStupid)
        self.assertTrue(IStupid.providedBy(v))

    def test_len(self):
        self.assertEqual(len(self.list_vocab), 3)
        self.assertEqual(len(self.items_vocab), 4)

    def test_contains(self):
        for v in (self.list_vocab, self.items_vocab):
            self.assertTrue(1 in v and 2 in v and 3 in v)
            self.assertTrue(5 not in v)

    def test_iter_and_get_term(self):
        for v in (self.list_vocab, self.items_vocab):
            for term in v:
                self.assertTrue(v.getTerm(term.value) is term)
                self.assertTrue(v.getTermByToken(term.token) is term)

    def test_nonunique_tokens(self):
        self.assertRaises(
            ValueError, vocabulary.SimpleVocabulary.fromValues,
            [2, '2'])
        self.assertRaises(
            ValueError, vocabulary.SimpleVocabulary.fromItems, 
            [(1, 'one'), ('1', 'another one')])
        self.assertRaises(
            ValueError, vocabulary.SimpleVocabulary.fromItems,
            [(0, 'one'), (1, 'one')])

    def test_nonunique_token_message(self):
        try:
            vocabulary.SimpleVocabulary.fromValues([2, '2'])
        except ValueError as e:
            self.assertEqual(str(e), "term tokens must be unique: '2'")

    def test_nonunique_token_messages(self):
        try:
            vocabulary.SimpleVocabulary.fromItems([(0, 'one'), (1, 'one')])
        except ValueError as e:
            self.assertEqual(str(e), "term values must be unique: 'one'")

    def test_overriding_createTerm(self):
        class MyTerm(object):
            def __init__(self, value):
                self.value = value
                self.token = repr(value)
                self.nextvalue = value + 1

        class MyVocabulary(vocabulary.SimpleVocabulary):
            def createTerm(cls, value):
                return MyTerm(value)
            createTerm = classmethod(createTerm)

        vocab = MyVocabulary.fromValues([1, 2, 3])
        for term in vocab:
            self.assertEqual(term.value + 1, term.nextvalue)


class TreeVocabularyTests(unittest.TestCase):
    region_tree = { 
            ('regions', 'Regions'): {
                ('aut', 'Austria'): {
                    ('tyr', 'Tyrol'): {
                        ('auss', 'Ausserfern'): {},
                    }
                },
                ('ger', 'Germany'): {
                    ('bav', 'Bavaria'):{}
                },
            }
        }
    tree_vocab_2 = vocabulary.TreeVocabulary.fromDict(region_tree)

    business_tree = {
            ('services', 'services', 'Services'): {
                ('reservations', 'reservations', 'Reservations'): {
                    ('res_host', 'res_host', 'Res Host'): {},
                    ('res_gui', 'res_gui', 'Res GUI'): {},
                },
                ('check_in', 'check_in', 'Check-in'): {
                    ('dcs_host', 'dcs_host', 'DCS Host'): {},
                },
            },
            ('infrastructure', 'infrastructure', 'Infrastructure'): {
                ('communication_network', 'communication_network', 'Communication/Network'): {
                    ('messaging', 'messaging', 'Messaging'): {},
                },
                ('data_transaction', 'data_transaction', 'Data/Transaction'): {
                    ('database', 'database', 'Database'): {},
                },
                ('security', 'security', 'Security'): {},
            },
        }
    tree_vocab_3 = vocabulary.TreeVocabulary.fromDict(business_tree)

    def test_implementation(self):
        for v in [self.tree_vocab_2, self.tree_vocab_3]:
            self.assertTrue(verifyObject(IEnumerableMapping, v))
            self.assertTrue(verifyObject(interfaces.IVocabulary, v))
            self.assertTrue(verifyObject(interfaces.IVocabularyTokenized, v))
            self.assertTrue(verifyObject(interfaces.ITreeVocabulary, v))

    def test_addt_interfaces(self):
        class IStupid(Interface):
            pass
        v = vocabulary.TreeVocabulary.fromDict({('one', '1'): {}}, IStupid)
        self.assertTrue(IStupid.providedBy(v))

    def test_ordering(self):
        """The TreeVocabulary makes use of an OrderedDict to store it's
           internal tree representation.

           Check that they keys are indeed oredered.
        """

        d = {   (1, 'new_york', 'New York'): {
                    (2, 'ny_albany', 'Albany'): {},
                    (3, 'ny_new_york', 'New York'): {},
                },
                (4, 'california', 'California'): {
                    (5, 'ca_los_angeles', 'Los Angeles'): {},
                    (6, 'ca_san_francisco', 'San Francisco'): {},
                },
                (7, 'texas', 'Texas'): {},
                (8, 'florida', 'Florida'): {},
                (9, 'utah', 'Utah'): {},
            }
        dict_ = OrderedDict(sorted(d.items(), key=lambda t: t[0]))
        vocab = vocabulary.TreeVocabulary.fromDict(dict_)
        # Test keys
        self.assertEqual([k.token for k in vocab.keys()], ['1', '4', '7', '8', '9'])
        # Test __iter__
        self.assertEqual([k.token for k in vocab], ['1', '4', '7', '8', '9'])

        self.assertEqual([k.token for k in vocab[[k for k in vocab.keys()][0]].keys()], ['2', '3'])
        self.assertEqual([k.token for k in vocab[[k for k in vocab.keys()][1]].keys()], ['5', '6'])

    def test_indexes(self):
        """ The TreeVocabulary creates three indexes for quick lookups,
        term_by_value, term_by_value and path_by_value.
        """
        self.assertEqual(
            [k for k in self.tree_vocab_2.term_by_value.keys()], 
            ['Tyrol', 'Bavaria', 'Regions', 'Austria', 'Germany', 'Ausserfern'])

        self.assertEqual(
            [k for k in self.tree_vocab_2.term_by_token.keys()],
            ['bav', 'ger', 'auss', 'regions', 'aut', 'tyr'])

        self.assertEqual(
            [k for k in self.tree_vocab_2.path_by_value.keys()], 
            ['Tyrol', 'Bavaria', 'Regions', 'Austria', 'Germany', 'Ausserfern'])

        self.assertEqual(
            [k for k in self.tree_vocab_2.path_by_value.values()], 
            [
                ['Regions', 'Austria', 'Tyrol'], 
                ['Regions', 'Germany', 'Bavaria'], 
                ['Regions'], 
                ['Regions', 'Austria'], 
                ['Regions', 'Germany'], 
                ['Regions', 'Austria', 'Tyrol', 'Ausserfern']
            ])

        self.assertEqual(
            [k for k in self.tree_vocab_3.term_by_value.keys()], 
            [   'data_transaction', 
                'check_in', 
                'infrastructure', 
                'res_gui', 
                'database', 
                'reservations', 
                'dcs_host', 
                'communication_network', 
                'res_host', 
                'services', 
                'messaging', 
                'security'
            ])

        self.assertEqual(
            [k for k in self.tree_vocab_3.term_by_token.keys()],
            [   'data_transaction', 
                'check_in', 
                'infrastructure', 
                'res_gui', 
                'database', 
                'reservations', 
                'dcs_host', 
                'communication_network', 
                'res_host', 
                'services', 
                'messaging', 
                'security'
            ])

        self.assertEqual(
            [k for k in self.tree_vocab_3.path_by_value.values()], 
            [   ['infrastructure', 'data_transaction'], 
                ['services', 'check_in'],
                ['infrastructure'], 
                ['services', 'reservations', 'res_gui'],
                ['infrastructure', 'data_transaction', 'database'], 
                ['services', 'reservations'], 
                ['services', 'check_in', 'dcs_host'],
                ['infrastructure', 'communication_network'], 
                ['services', 'reservations', 'res_host'], 
                ['services'], 
                ['infrastructure', 'communication_network', 'messaging'], 
                ['infrastructure', 'security']
            ])

    def test_termpath(self):
        self.assertEqual(
                    self.tree_vocab_2.getTermPath('Bavaria'), 
                    ['Regions', 'Germany', 'Bavaria'])
        self.assertEqual(
                    self.tree_vocab_2.getTermPath('Austria'), 
                    ['Regions', 'Austria'])
        self.assertEqual(
                    self.tree_vocab_2.getTermPath('Ausserfern'), 
                    ['Regions', 'Austria', 'Tyrol', 'Ausserfern'])
        self.assertEqual(
                    self.tree_vocab_2.getTermPath('Non-existent'), 
                    [])
        self.assertEqual(
                    self.tree_vocab_3.getTermPath('database'),
                    ["infrastructure", "data_transaction", "database"])

    def test_len(self):
        """ len returns the number of all nodes in the dict
        """
        self.assertEqual(len(self.tree_vocab_2), 1)
        self.assertEqual(len(self.tree_vocab_3), 2)

    def test_contains(self):
        self.assertTrue('Regions' in self.tree_vocab_2 and 
                        'Austria' in self.tree_vocab_2 and 
                        'Bavaria' in self.tree_vocab_2)

        self.assertTrue('bav' not in self.tree_vocab_2)
        self.assertTrue('foo' not in self.tree_vocab_2)

        self.assertTrue('database' in self.tree_vocab_3 and 
                        'security' in self.tree_vocab_3 and 
                        'services' in self.tree_vocab_3)

        self.assertTrue('Services' not in self.tree_vocab_3)
        self.assertTrue('Database' not in self.tree_vocab_3)

    def test_values_and_items(self):
        for v in (self.tree_vocab_2, self.tree_vocab_3):
            for term in v:
                self.assertEqual([i for i in v.values()], [i for i in v._terms.values()])
                self.assertEqual([i for i in v.items()], [i for i in v._terms.items()])

    def test_get(self):
        for v in [self.tree_vocab_2, self.tree_vocab_3]:
            for key, value in v.items():
                self.assertEqual(v.get(key), value)
                self.assertEqual(v[key], value)

    def test_get_term(self):
        for v in (self.tree_vocab_2, self.tree_vocab_3):
            for term in v:
                self.assertTrue(v.getTerm(term.value) is term)
                self.assertTrue(v.getTermByToken(term.token) is term)
            self.assertRaises(LookupError, v.getTerm, 'non-present-value')
            self.assertRaises(LookupError, v.getTermByToken, 'non-present-token')

    def test_nonunique_values_and_tokens(self):
        """Since we do term and value lookups, all terms' values and tokens
        must be unique. This rule applies recursively.
        """
        self.assertRaises(
            ValueError, vocabulary.TreeVocabulary.fromDict,
            { ('one', '1'): {},
              ('two', '1'): {},
            })
        self.assertRaises(
            ValueError, vocabulary.TreeVocabulary.fromDict,
            { ('one', '1'): {},
              ('one', '2'): {},
            })
        # Even nested tokens must be unique.
        self.assertRaises(
            ValueError, vocabulary.TreeVocabulary.fromDict,
            { ('new_york', 'New York'): {
                    ('albany', 'Albany'): {},
                    ('new_york', 'New York'): {},
                },
            })
        # The same applies to nested values.
        self.assertRaises(
            ValueError, vocabulary.TreeVocabulary.fromDict,
            { ('1', 'new_york'): {
                    ('2', 'albany'): {},
                    ('3', 'new_york'): {},
                },
            })
        # The title attribute does however not have to be unique.
        vocabulary.TreeVocabulary.fromDict(
            { ('1', 'new_york', 'New York'): {
                    ('2', 'ny_albany', 'Albany'): {},
                    ('3', 'ny_new_york', 'New York'): {},
                },
            })
        vocabulary.TreeVocabulary.fromDict({
                ('one', '1', 'One'): {},
                ('two', '2', 'One'): {},
            })

    def test_nonunique_value_message(self):
        try:
            vocabulary.TreeVocabulary.fromDict(
            { ('one', '1'): {},
              ('two', '1'): {},
            })
        except ValueError as e:
            self.assertEqual(str(e), "Term values must be unique: '1'")

    def test_nonunique_token_message(self):
        try:
            vocabulary.TreeVocabulary.fromDict(
            { ('one', '1'): {},
              ('one', '2'): {},
            })
        except ValueError as e:
            self.assertEqual(str(e), "Term tokens must be unique: 'one'")

    def test_recursive_methods(self):
        """Test the _createTermTree and _getPathToTreeNode methods
        """
        tree = vocabulary._createTermTree({}, self.business_tree)
        vocab = vocabulary.TreeVocabulary.fromDict(self.business_tree)

        term_path = vocab._getPathToTreeNode(tree, "infrastructure")
        vocab_path = vocab._getPathToTreeNode(vocab, "infrastructure")
        self.assertEqual(term_path, vocab_path)
        self.assertEqual(term_path, ["infrastructure"])

        term_path = vocab._getPathToTreeNode(tree, "security")
        vocab_path = vocab._getPathToTreeNode(vocab, "security")
        self.assertEqual(term_path, vocab_path)
        self.assertEqual(term_path, ["infrastructure", "security"])

        term_path = vocab._getPathToTreeNode(tree, "database")
        vocab_path = vocab._getPathToTreeNode(vocab, "database")
        self.assertEqual(term_path, vocab_path)
        self.assertEqual(term_path, ["infrastructure", "data_transaction", "database"])

        term_path = vocab._getPathToTreeNode(tree, "dcs_host")
        vocab_path = vocab._getPathToTreeNode(vocab, "dcs_host")
        self.assertEqual(term_path, vocab_path)
        self.assertEqual(term_path, ["services", "check_in", "dcs_host"])

        term_path = vocab._getPathToTreeNode(tree, "dummy")
        vocab_path = vocab._getPathToTreeNode(vocab, "dummy")
        self.assertEqual(term_path, vocab_path)
        self.assertEqual(term_path, [])

def test_suite():
    suite = unittest.makeSuite(RegistryTests)
    suite.addTest(unittest.makeSuite(SimpleVocabularyTests))
    suite.addTest(unittest.makeSuite(TreeVocabularyTests))
    return suite

if __name__ == "__main__":
    unittest.main(defaultTest="test_suite")


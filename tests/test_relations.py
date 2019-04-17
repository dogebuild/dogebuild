from unittest import TestCase

from dogebuild.relations import RelationManager


class TestRelationManager(TestCase):
    def test_dependencies(self):
        rm = RelationManager()

        rm.add_dependency('Coffee', ['Beans', 'Milk', 'Water'])
        rm.add_dependency('Tea', ['Leafs', 'Water', 'Lemon'])
        rm.add_dependency('Water', ['Fire'])

        self.assertListEqual(
            rm.get_dependencies_recursive(['Water']),
            ['Fire', 'Water']
        )

        coffeeList = rm.get_dependencies_recursive(['Coffee'])
        self.assertLess(coffeeList.index('Fire'), coffeeList.index('Water'))
        self.assertEqual(coffeeList[-1], 'Coffee')

        teaList = rm.get_dependencies_recursive(['Tea'])
        self.assertLess(teaList.index('Fire'), coffeeList.index('Water'))
        self.assertEqual(teaList[-1], 'Tea')

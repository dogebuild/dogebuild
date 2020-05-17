from unittest import TestCase

from dogebuild.dogefile_internals.relations import RelationManager


class TestRelationManager(TestCase):
    def test_dependencies(self):
        rm = RelationManager()

        rm.add_dependency("Coffee", ["Beans", "Milk", "Water"])
        rm.add_dependency("Tea", ["Leafs", "Water", "Lemon"])
        rm.add_dependency("Water", ["Fire"])

        self.assertListEqual(rm.get_dependencies_recursive(["Water"]), ["Fire", "Water"])

        coffee_list = rm.get_dependencies_recursive(["Coffee"])
        self.assertLess(coffee_list.index("Fire"), coffee_list.index("Water"))
        self.assertEqual(coffee_list[-1], "Coffee")

        tea_list = rm.get_dependencies_recursive(["Tea"])
        self.assertLess(tea_list.index("Fire"), coffee_list.index("Water"))
        self.assertEqual(tea_list[-1], "Tea")

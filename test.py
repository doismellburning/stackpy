import doctest
import unittest
import stackpy

def load_tests(loader, tests, pattern):
    tests.addTests(doctest.DocTestSuite(stackpy))
    tests.addTests(doctest.DocFileSuite('README.md'))
    return tests

class TestStackpy(unittest.TestCase):
    """
    These tests all depend on being able to reach the StackExchange API.

    TODO Sort some mocks such that this dependency is removed? Running on Travis would be nice
    """

    ME = 928098

    def setUp(self):
        self.stackpy = stackpy.Stackpy()

    def test_users(self):
        self.stackpy.users()

    def test_users_by_id(self):
        users = self.stackpy.users([self.ME])
        self.assertEqual(len(users.items), 1)
        user = users.items[0]
        #print user.__dict__
        self.assertEqual(user.user_id, self.ME)
        self.assertIn('Kristian', user.display_name)

    def test_sites(self):
        sites = self.stackpy.sites().items
        self.assertGreater(len(sites), 0)

    def test_users_by_no_id(self):
        users = self.stackpy.users([])
        self.assertEqual(users.items, [])

if __name__ == '__main__':
    unittest.main()

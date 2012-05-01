import unittest
import stackpy

class TestStackpy(unittest.TestCase):
    """
    These tests all depend on being able to reach the StackExchange API.

    TODO Sort some mocks such that this dependency is removed? Running on Travis would be nice
    """
    def setUp(self):
        self.stackpy = stackpy.Stackpy()

    def test_users(self):
        self.stackpy.users()

    def test_users_by_id(self):
        ME = 928098
        users = self.stackpy.users([ME])
        self.assertEqual(len(users.items), 1)
        user = users.items[0]
        #print user.__dict__
        self.assertEqual(user.user_id, ME)
        self.assertIn('Kristian', user.display_name)

    def test_sites(self):
        sites = self.stackpy.sites().items
        self.assertGreater(len(sites), 0)

if __name__ == '__main__':
    unittest.main()

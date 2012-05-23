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

    def test_my_badges(self):
        me = self.stackpy.users([self.ME]).items[0]
        my_badges = me.badges().items
        self.assertGreater(len(my_badges), 5)

    def test_join_ids(self):
        self.assertEqual(stackpy._join_ids([1,2,3]), '1;2;3')
        self.assertEqual(stackpy._join_ids(['1','2','3']), '1;2;3')

    def test_join_bad_ids(self):
        try:
            bad_ids = ['goat']
            bad = stackpy._join_ids(bad_ids)
            self.fail('Should barf attempting to join %s (instead got %s)' % (bad_ids, bad))
        except ValueError:
            pass

    def test_paging(self):
        # We'll assume I'll never have this many badges...
        r = self.stackpy.user_badges([self.ME], page=1000)
        self.assertFalse(r.has_more)
        self.assertEqual(r.items, [])

if __name__ == '__main__':
    unittest.main()

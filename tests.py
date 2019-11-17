from preference_creator import PreferenceCreator
import mock
import unittest
import numpy as np

# TODO: 
"""
Generate some sample voting schemes (deterministically and random)
Run all voting schemes on it
"""

class TestInputFunctions(unittest.TestCase):

    def test_get_number_of_voters_succ(self):
        pc = PreferenceCreator()
        number_of_voters = 2
        with mock.patch("builtins.input", return_value=str(number_of_voters)):
            pc.get_number_of_voters()    
            self.assertEqual(pc.number_of_voters, number_of_voters)
        with mock.patch("builtins.input", return_value="a"):
            with self.assertRaises(ValueError):
                pc.get_number_of_voters()      

    def test_get_number_of_candidates(self):
        pc = PreferenceCreator()
        number_of_candidates = 4
        with mock.patch("builtins.input", return_value=number_of_candidates):
            pc.get_number_of_candidates()
            self.assertEqual(pc.number_of_candidates, number_of_candidates)
        with mock.patch("builtins.input", return_value="a"):
            with self.assertRaises(ValueError):
                pc.get_number_of_candidates()
    
    def test_get_voter_cadidates(self):
        # deterministic
        # 1 candidate
        # 1 voter
        pc = PreferenceCreator()
        pc.number_of_voters = 1
        pc.number_of_candidates = 1
        pc.list_of_candidates = ["A"]
        pc.preference_matrix = np.zeros((1, 1))
        with mock.patch("builtins.input", return_value="A"):
            pc.get_voter_candidates()
            self.assertEqual(pc.preference_matrix, np.array([65]).reshape(1, 1))

    # # ideally:
    # random
    # 10 candidates
    # 100 voters

if __name__ == "__main__":
    unittest.main()


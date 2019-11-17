from preference_creator import PreferenceCreator
from voting_schemes_runner import VotingSchemesRunner
import mock
import unittest
import numpy as np


def simple_test_scheme():
    pc = PreferenceCreator()
    pc.number_of_voters = 4
    pc.number_of_candidates = 4
    pc.list_of_candidates = ["A", "B", "C", "D"]
    pc.preference_matrix = np.array([[65, 65, 65, 65],
                                     [66, 66, 66, 66],
                                     [67, 67, 67, 67],
                                     [68, 68, 68, 68]])
    return pc


# class TestInputFunctions(unittest.TestCase):
#     """Generate some sample voting schemes (deterministically and random)"""
#     def test_get_number_of_voters_succ(self):
#         pc = PreferenceCreator()
#         number_of_voters = 2
#         with mock.patch("builtins.input", return_value=str(number_of_voters)):
#             pc.get_number_of_voters()    
#             self.assertEqual(pc.number_of_voters, number_of_voters)
#         with mock.patch("builtins.input", return_value="a"):
#             with self.assertRaises(ValueError):
#                 pc.get_number_of_voters()      

#     def test_get_number_of_candidates(self):
#         pc = PreferenceCreator()
#         number_of_candidates = 4
#         with mock.patch("builtins.input", return_value=number_of_candidates):
#             pc.get_number_of_candidates()
#             self.assertEqual(pc.number_of_candidates, number_of_candidates)
#         with mock.patch("builtins.input", return_value="a"):
#             with self.assertRaises(ValueError):
#                 pc.get_number_of_candidates()
    
#     def test_get_voter_cadidates(self):
#         # deterministic
#         # 1 candidate
#         # 1 voter
#         pc = PreferenceCreator()
#         pc.number_of_voters = 1
#         pc.number_of_candidates = 1
#         pc.list_of_candidates = ["A"]
#         pc.preference_matrix = np.zeros((1, 1))
#         with mock.patch("builtins.input", return_value="A"):
#             pc.get_voter_candidates()
#             self.assertEqual(pc.preference_matrix, np.array([65]).reshape(1, 1))

    # # ideally:
    # random
    # 10 candidates
    # 100 voters

class TestVotingSchemes(unittest.TestCase):
    """Perform Voting on selected test cases"""

    def test_plurality_voting(self):
        pc = simple_test_scheme()
        vsr = VotingSchemesRunner()
        desired_outcome = {65: 4, 66: 0, 67: 0, 68: 0}
        self.assertEqual(vsr.plurality_voting(pc.preference_matrix), desired_outcome)

    def test_voting_for_two(self):
        pc = simple_test_scheme()
        vsr = VotingSchemesRunner()
        desired_outcome = {65: 4, 66: 4, 67: 0, 68: 0}
        self.assertEqual(vsr.voting_for_two(pc.preference_matrix), desired_outcome)

    def test_borda_voting(self):
        pc = simple_test_scheme()
        vsr = VotingSchemesRunner()
        desired_outcome = {65: 12, 66: 8, 67: 4, 68: 0}
        self.assertEqual(vsr.borda_voting(pc.preference_matrix), desired_outcome)

    def test_anti_plurality_voting(self):
        pc = simple_test_scheme()
        vsr = VotingSchemesRunner()
        desired_outcome = {65: 4, 66: 4, 67: 4, 68: 0}
        self.assertEqual(vsr.anti_plurality_voting(pc.preference_matrix), desired_outcome)

if __name__ == "__main__":
    unittest.main()


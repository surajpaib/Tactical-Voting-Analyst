from preference_creator import PreferenceCreator as PC
from voting_schemes_runner import VotingSchemesRunner as VSR
from tactical_voting import TacticalVoting as TV
from collections import OrderedDict
import mock
import unittest
import numpy as np


def simple_test_scheme():
    pc = PC()
    pc.num_voters = 4
    pc.num_candidates = 4
    pc.candidate_list = ["A", "B", "C", "D"]
    pc.pref_mat = np.array([[65, 65, 65, 65],
                                     [66, 66, 66, 66],
                                     [67, 67, 67, 67],
                                     [68, 68, 68, 68]])
    return pc


class TestInputFunctions(unittest.TestCase):
    """Generate some sample voting schemes (deterministically and random)"""
    def test_get_num_voters_succ(self):
        pc = PC()
        num_voters = 2
        with mock.patch("builtins.input", return_value=str(num_voters)):
            pc.get_num_voters()    
            self.assertEqual(pc.num_voters, num_voters)
        with mock.patch("builtins.input", return_value="a"):
            with self.assertRaises(ValueError):
                pc.get_num_voters()      

    def test_get_num_candidates(self):
        pc = PC()
        num_candidates = 4
        with mock.patch("builtins.input", return_value=num_candidates):
            pc.get_num_candidates()
            self.assertEqual(pc.num_candidates, num_candidates)
            self.assertEqual(pc.candidate_list, ["A", "B", "C", "D"])
            self.assertTrue((pc.pref_mat == np.array([]).reshape(4, 0)).all())
        with mock.patch("builtins.input", return_value="a"):
            with self.assertRaises(ValueError):
                pc.get_num_candidates()

    def test_get_voting_schemes(self):
        pc = PC()
        with mock.patch("builtins.input", return_value=1):
            pc.get_voting_schemes()
            self.assertEqual(pc.scheme, 0)
    
    def test_get_voter_cadidates(self):
        pc = PC()
        pc.num_voters = 1
        pc.num_candidates = 1
        pc.candidate_list = ["A"]
        pc.pref_mat = np.zeros((1, 1))
        with mock.patch("builtins.input", return_value="A"):
            pc.get_voter_candidates()
            self.assertEqual(pc.pref_mat, np.array([65]).reshape(1, 1))

    # # ideally:
    # random
    # 10 candidates
    # 100 voters

class TestVotingSchemes(unittest.TestCase):
    """Perform Voting on selected test cases"""

    def test_plurality_voting(self):
        pc = simple_test_scheme()
        vsr = VSR()
        desired_outcome = {65: 4, 66: 0, 67: 0, 68: 0}
        self.assertEqual(vsr.plurality_voting(pc.pref_mat), desired_outcome)

    def test_voting_for_two(self):
        pc = simple_test_scheme()
        vsr = VSR()
        desired_outcome = {65: 4, 66: 4, 67: 0, 68: 0}
        self.assertEqual(vsr.voting_for_two(pc.pref_mat), desired_outcome)

    def test_borda_voting(self):
        pc = simple_test_scheme()
        vsr = VSR()
        desired_outcome = {65: 12, 66: 8, 67: 4, 68: 0}
        self.assertEqual(vsr.borda_voting(pc.pref_mat), desired_outcome)

    def test_anti_plurality_voting(self):
        pc = simple_test_scheme()
        vsr = VSR()
        desired_outcome = {65: 4, 66: 4, 67: 4, 68: 0}
        self.assertEqual(vsr.anti_plurality_voting(pc.pref_mat), desired_outcome)

    def test_calculate_voter_happiness(self):
        pref_mat = np.array([65, 66, 67, 68]).reshape(-1, 1)
        voting_outcome = {66: 4, 65: 0, 67: 0, 68: 0}
        vsr = VSR()
        desired_outcome = 1 / (1 + abs(4*(3-4) + 3*(4-3) + 2*(2-2) + 1*(1-1)))
        self.assertEqual(vsr.get_happiness(pref_mat, voting_outcome), np.array([desired_outcome]))

    def test_calculate_voter_happiness2(self):
        pref_mat = np.array([65, 66, 67, 68]).reshape(-1, 1)
        voting_outcome = {65: 4, 66: 0, 67: 0, 68: 0}
        vsr = VSR()
        desired_outcome = 1 / (1 + abs(4*(4-4) + 3*(3-3) + 2*(2-2) + 1*(1-1)))
        self.assertEqual(vsr.get_happiness(pref_mat, voting_outcome), np.array([desired_outcome]))
    
    def test_calculate_voter_happiness3(self):
        pref_mat = np.array([65, 66, 67, 68]).reshape(-1, 1)
        voting_outcome = {68: 4, 66: 0, 67: 0, 65: 0}
        vsr = VSR()
        desired_outcome = 1 / (1 + abs(4*(1-4) + 3*(3-3) + 2*(2-2) + 1*(4-1)))
        self.assertEqual(vsr.get_happiness(pref_mat, voting_outcome), np.array([desired_outcome]))

    def test_calculate_voter_happiness4(self):
        pref_mat = np.array([65, 66, 67, 68]).reshape(-1, 1)
        voting_outcome = {68: 4, 67: 0, 66: 0, 65: 0}
        vsr = VSR()
        desired_outcome = 1 / (1 + abs(4*(1-4) + 3*(2-3) + 2*(3-2) + 1*(4-1)))
        self.assertEqual(vsr.get_happiness(pref_mat, voting_outcome), np.array([desired_outcome]))

    def test_calculate_overall_happiness(self):
        pass


if __name__ == "__main__":
    unittest.main()


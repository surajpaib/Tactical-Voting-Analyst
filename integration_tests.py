from preference_creator import PreferenceCreator as PC
from voting_schemes_runner import VotingSchemesRunner as VSR
from tactical_voting import TacticalVoting as TV
from itertools import permutations
import numpy as np

def integration_MxN(n_candidates, n_voters, voting_scheme):
    """
    @param voting_scheme: one of the four voting schemes
    """
    candidates_num = range(65, 65+n_candidates)
    candidates = [str(chr(i)) for i in candidates_num]
    pref_list = list(permutations(candidates_num))
    pref_mat = np.zeros((n_candidates, n_voters), dtype=np.uint8)
    for i in range(n_voters):
        rand = np.random.randint(0, len(pref_list))
        pref_mat[:, i] = np.array(pref_list[rand])
    params = {"num_voters": n_voters,
              "num_candidates": n_candidates,
              "candidate_list": candidates,
              "pref_mat": pref_mat,
              "scheme": voting_scheme}  # scheme is not 2 as in manual selection
    pc = PC(**params)
    vsr = VSR()
    vsr.voting_simulation(pc.pref_mat, pc.scheme)
    tv = TV(pref_mat=pc.pref_mat,
            voting_outcome=vsr.results,
            scheme=pc.scheme)
    return pc, vsr, tv

def integration_voting_for_two():
    """Integration test for voting_for_two"""
    params = {"num_voters": 3,
              "num_candidates": 2,
              "candidate_list": ["A", "B"],
              "pref_mat": np.array([[65, 66, 65], [66, 65, 66]]),
              "scheme": 1}  # scheme is not 2 as in manual selection
    pc = PC(**params)
    vsr = VSR()
    vsr.voting_simulation(pc.pref_mat, pc.scheme)
    tv = TV(pref_mat=pc.pref_mat,
            voting_outcome=vsr.results,
            scheme=pc.scheme)
    """Expected outcome: Bullet voting as well as compromising possible for all"""
    return pc, vsr, tv
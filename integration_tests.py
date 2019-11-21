from preference_creator import PreferenceCreator as PC
from voting_schemes_runner import VotingSchemesRunner as VSR
from tactical_voting import TacticalVoting as TV
import numpy as np

def integration_voting_for_two():
    """
    Integration test for voting_for_two
    @param pc: PC
    @param vsr: VotingSchemeRunner
    @param tv: TacticalVoter
    """
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
    """Expected outcome: Bullet voting possible for candidate 2"""
    return pc, vsr, tv
"""
1) Experiments on strategic voting risk depending on number of voters and number of candidates
2) Experiments on runtime limitatiosn
"""

from preference_creator import PreferenceCreator as PC
from voting_schemes_runner import VotingSchemesRunner as VSR
from tactical_voting import TacticalVoting as TV
from itertools import permutations
import integration_tests
import numpy as np
import pandas as pd
import os

def experiment(max_n_candidates, max_n_voters):
    target_dir = "experiments"
    target_file = "experiments/log.csv"
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    if not os.path.exists(target_file):
        df = pd.DataFrame({
            "voting_scheme": [],
            "n_voters": [],
            "n_candidates": [],
            "strat_voting_risk": [],
            "avg_happiness": []
        })
        df.to_csv(target_file, index=False)
    else:
        df = pd.read_csv(target_file)

    voting_schemes = ['1: Plurality Voting', '2: Voting for two', '3: Anti-Plurality Voting', '4: Borda Voting']
    vs_list = []
    v_list = []
    c_list = []
    strat_voting_list = []
    happiness_list = []
    # TODO: fix error here!
    for vs in range(4):  # voting schemes:
        for c in range(max_n_candidates):
            for v in range(max_n_voters):
                pc, vsr, tv = integration_tests.integration_MxN(c, v, vs)
                avg_happiness = sum(vsr.get_happiness(pc.pref_mat, vsr.results))/v
                tv.bullet_voting()       
                tv.compromising_strategy()
                strat_voting_risk = sum([1 if len(i)>0 else 0 for i in tv.strategic_voting_options]) /pc.num_voters
                
                vs_list.append(voting_schemes[vs])
                v_list.append(v)
                c_list.append(c)
                strat_voting_list.append(strat_voting_risk)
                happiness_list.append(avg_happiness)

    df_new = pd.DataFrame({
            "voting_scheme": vs_list,
            "n_voters": v_list,
            "n_candidates": c_list,
            "strat_voting_risk": strat_voting_list,
            "avg_happiness": happiness_list
        })
    df_overall = pd.concat((df, df_new), axis=0)
    df_overall.to_csv(target_file)


def visualize():
    """Visualize experiment data per voting schme"""
    pass





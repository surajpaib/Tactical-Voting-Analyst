from voting_schemes_runner import VotingSchemesRunner as VSR
from itertools import permutations
from copy import deepcopy
from collections import OrderedDict
import numpy as np


class TacticalVoting:
    def __init__(self, pref_mat, voting_outcome, scheme):
        self.pref_mat = pref_mat
        self.voting_outcome = voting_outcome
        self.vsr = VSR()
        self.scheme = scheme
        self.n_candidates = pref_mat.shape[0]
        self.n_voters = pref_mat.shape[1]
        self.strategic_voting_options = [[] for _ in range(self.n_voters)]

    def bullet_voting(self):
        """Calculate whether voting for just one of the alternatives can result in greater happiness"""

        # bullet voting can be applied, but it will not achieve anything
        # if self.scheme == 0:
            # print("Bullet voting cannot be applied to plurality voting.")

        happiness = self.vsr.get_happiness(self.pref_mat, self.voting_outcome)
        for voter in range(self.n_voters):
            for candidate in np.unique(self.pref_mat):
                # voter i attempts tactical voting for each possible candicate
                bullet_pref_mat = np.copy(self.pref_mat)
                bullet_pref_mat[1:, voter] = 0
                bullet_pref_mat[0, voter] = candidate

                tactical_results = self.vsr.voting_simulation(bullet_pref_mat, self.scheme)
                del tactical_results[0]  # Delete the '0' candidate
                tactical_happiness = self.vsr.get_happiness(self.pref_mat, tactical_results)
                happiness_gain = tactical_happiness[voter] - happiness[voter]
                str_tactical_results = dict(zip([chr(i) for i in tactical_results.keys()], tactical_results.values()))
                if happiness_gain > 0:
                    voter_num = voter +1
                    print_gain = np.round(happiness_gain, 3)
                    self.strategic_voting_options[voter].append({
                        "Preference list": [chr(i).replace('\x00','') for i in bullet_pref_mat[:, voter]],
                        "Voting result": deepcopy(str_tactical_results),
                        "New happiness": np.copy(sum(tactical_happiness)),
                        "Description": "Happiness of voter {} increased by : {} due to voting only for {}".format(
                            voter_num, print_gain, chr(candidate))
                    })

    def compromising_strategy(self):
        """Tactical voting by ranking alternatives insincerely higher (lower)"""
        happiness = self.vsr.get_happiness(self.pref_mat, self.voting_outcome)

        for voter in range(self.n_voters):
            for c1 in range(self.n_candidates):  # candidate 1
                for c2 in range(self.n_candidates):  # candidate 2
                    # tactic: swap candidates c1 and c2
                    if (c1 >= c2):
                        continue
                    comp_pref = np.copy(self.pref_mat)                    
                    comp_pref[c1, voter], comp_pref[c2, voter] = comp_pref[c2, voter], comp_pref[c1, voter]
                    tactical_results = self.vsr.voting_simulation(comp_pref, self.scheme)
                    tactical_happiness = self.vsr.get_happiness(self.pref_mat, tactical_results)
                    happiness_gain = tactical_happiness[voter] - happiness[voter]
                    str_tactical_results = dict(zip([chr(i) for i in tactical_results.keys()], tactical_results.values()))
                    if happiness_gain > 0:
                        c1_name = chr(self.pref_mat[c1, voter])
                        c2_name = chr(self.pref_mat[c2, voter])
                        voter_num = voter +1
                        print_gain = np.round(happiness_gain, 3)
                        self.strategic_voting_options[voter].append({
                            "Preference list": [chr(i) for i in comp_pref[:, voter]],
                            "Voting results": deepcopy(str_tactical_results),
                            "New happiness": np.copy(sum(tactical_happiness)),
                            "Description": "Happiness of voter {} increased by {} due to swapping {} with {}".format(
                                voter_num, print_gain, c1_name, c2_name)                       
                        })

    def compromising_strategy_permutations(self):
        """Compromising using permutations"""
        happiness = self.vsr.get_happiness(self.pref_mat, self.voting_outcome)
        for voter in range(self.n_voters):
            # create (n_candidates!)x(n_candidates) permutation matrix
            permutation_mat = np.array(list(permutations(self.pref_mat[:, voter])))
            for i in range(permutation_mat.shape[0]):
                comp_pref = np.copy(self.pref_mat)
                comp_pref[:, voter] = permutation_mat[i, :]

                tactical_results = self.vsr.voting_simulation(comp_pref, self.scheme)
                tactical_happiness = self.vsr.get_happiness(comp_pref, tactical_results)
                happiness_gain = tactical_happiness[voter] - happiness[voter]
                str_tactical_results = dict(zip([chr(i) for i in tactical_results.keys()], tactical_results.values()))
                if happiness_gain > 0:
                    voter_num = voter +1
                    print_gain = np.round(happiness_gain, 3)
                    self.strategic_voting_options[voter].append({
                        "Preference list": [chr(i) for i in comp_pref[:, voter]],
                        "Voting results": deepcopy(str_tactical_results),
                        "New happiness": np.copy(sum(tactical_happiness)),
                        "Description": "Happiness of voter {} increased by : {} due to reordering of preferences".format(
                                voter_num, print_gain)  
                    })


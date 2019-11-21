from voting_schemes_runner import VotingSchemesRunner as VSR
from itertools import permutations
import numpy as np

class TacticalVoting:
    def __init__(self, pref_mat, voting_outcome, scheme):
        self.pref_mat = pref_mat
        self.voting_outcome = voting_outcome
        self.vsr = VSR()
        self.scheme = scheme
        self.n_candidates = pref_mat.shape[0]
        self.n_voters = pref_mat.shape[1]
        self.strategic_voting_options = [[]] * self.n_voters

    def bullet_voting(self):
        """Calculate whether voting for just one of the alternatives can result in greater happiness"""

        if self.scheme == 0:
            print("Bullet voting cannot be applied to plurality voting.")
            exit()  

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
                if happiness_gain > 0:
                    self.strategic_voting_options[voter].append((
                        bullet_pref_mat,
                        tactical_results,
                        sum(tactical_happiness),
                        "Happiness of voter {} increased by : {} due to voting only for {}".format(voter, happiness_gain, str(candidate))
                    ))

    def compromising_strategy(self):
        """Tactical voting by ranking alternatives insincerely higher (lower)"""
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
                if happiness_gain > 0:
                    self.strategic_voting_options[voter].append((
                        comp_pref,
                        tactical_results,
                        sum(tactical_happiness),
                        "Happiness of voter {} increased by : {} due to reordering of preferences".format(
                            voter, happiness_gain)                        
                    ))

        ## Corrected, but still not what we want
        # for voter in range(len(self.n_voters)):
        #     for c1 in range(len(self.n_candidates)):  # candidate 1
        #         for c2 in range(len(self.n_candidates)):  # candidate 2
        #             # tactic: swap candidates c1 and c2
        #             if c1==c2:
        #                 continue
        #             comp_pref = np.copy(self.pref_mat)                    
        #             tmp = comp_pref[c1, voter]
        #             comp_pref[c1, voter] = comp_pref[c2, voter]
        #             comp_pref[c2, voter] = tmp

        #             tactical_results = self.vsr.voting_simulation(comp_pref, self.scheme)
        #             tactical_happiness = self.vsr.get_happiness(comp_pref, tactical_results)
        #             happiness_gain = tactical_happiness[voter] - happiness[voter]
        #             if happiness_gain > 0:
        #                 self.strategic_voting_options[voter].append((
        #                     comp_pref,
        #                     tactical_results,
        #                     sum(tactical_happiness),
        #                     "Happiness of voter {} increased by : {} due to swapping {} with {}".format(
        #                         voter, happiness_gain, c1, c2)                        
        #                 ))

        ## WRONG
        # modified_pref_mat = [[]] * len(self.n_candidates)
        # for i in range(len(self.n_candidates)):
        #     for j in range(self.n_voters):
        #         for k in range(self.n_voters):
        #             if k != j:
        #                 pref2 = np.copy(self.pref_mat)
        #                 tmp = pref2[j,i]
        #                 pref2[j,i] = pref2[k,i]
        #                 pref2[k,i] = tmp
        #                 tactical_results = self.vsr.voting_simulation(pref2, self.scheme)
        #                 new_happiness = self.vsr.get_happiness(pref2, tactical_results)
        #                 happiness_gain = new_happiness[i] - happiness[i]
        #                 if (happiness[i] < new_happiness[i]):
        #                     modified_pref_mat[i] = np.copy(pref2)
        #                 # if (calculate happiness>): pref2 = modified_pref_mat
        # return modified_pref_mat
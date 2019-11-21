from voting_schemes_runner import VotingSchemesRunner as VSR
from copy import copy, deepcopy
import numpy as np

class TacticalVoting:
    def __init__(self, pref_mat, voting_outcome, scheme):
        self.pref_mat = pref_mat
        self.voting_outcome = voting_outcome
        self.vsr = VSR()
        self.scheme = scheme
        self.n_candidates = pref_mat.shape[0]
        self.n_voters = pref_mat.shape[1]
        self.strategic_voting_options = [()] * self.n_voters

    def bullet_voting(self):
        """Calculate whether voting for just one of the alternatives can result in greater happiness"""

        if self.scheme == 0:
            print("Bullet voting cannot be applied to plurality voting.")
            return False        

        # TODO: why for i in range(self.n_candidates) ?
        happiness = self.vsr.get_happiness(self.pref_mat, self.voting_outcome)
        for i in range(self.pref_mat.shape[1]):
            for candidate in np.unique(self.pref_mat):
                # voter i attempts tactical voting for each possible candicate
                bullet_pref_mat = np.copy(self.pref_mat)
                bullet_pref_mat[1:, i] = 0
                bullet_pref_mat[0, i] = candidate

                tactical_results = self.vsr.voting_simulation(bullet_pref_mat, self.scheme)
                del tactical_results[0]  # Delete the '0' candidate
                happiness_tactical = self.vsr.get_happiness(self.pref_mat, tactical_results)
                happiness_gain = happiness_tactical[i] - happiness[i]
                if happiness_gain > 0:
                    self.strategic_voting_options[i] = (
                        bullet_pref_mat,
                        tactical_results,
                        sum(happiness_tactical),
                        "Happiness of voter {} increased by : {} due to voting only for {}".format(i, happiness_gain, candidate)
                    )
        return True

    def compromising_strategy(self, pref_mat, voting_outcome):
        self.happiness = self.vsr.get_happiness(pref_mat, voting_outcome)
        self.modified_pref_mat = [[]] * len(pref_mat[0])
        
        for i in range(len(pref_mat[0])):
            for j in range(len(pref_mat[:,0])):
                for k in range(len(pref_mat[:,0])):
                    if k != j:
                        self.pref2 = deepcopy(pref_mat)
                        tmp = self.pref2[j,i]
                        self.pref2[j,i] = self.pref2[k,i]
                        self.pref2[k,i] = tmp
                        tactical_results = self.vsr.voting_simulation(self.pref2, self.scheme)
                        self.new_happiness = self.vsr.get_happiness(self.pref2, tactical_results)
                        #print("\nInit VH : {}, new VH: {}".format(self.happiness,self.new_happiness))
                        if (self.happiness[i] < self.new_happiness[i]):
                            self.modified_pref_mat[i] = deepcopy(self.pref2)
                        # if (calculate happiness>): pref2 = modified_pref_mat
        return self.modified_pref_mat
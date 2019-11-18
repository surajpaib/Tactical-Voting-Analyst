from voting_schemes_runner import VotingSchemesRunner
from copy import copy, deepcopy
import numpy as np

class TacticalVoting:
    def __init__(self, preference_matrix, voting_outcome, selected_scheme):
        self.preference_matrix = preference_matrix
        self.voting_outcome = voting_outcome
        self.votingrunner = VotingSchemesRunner()
        self.selected_scheme = selected_scheme

        self.n_candidates = preference_matrix.shape[0]
        self.strategic_voting_options = [[]] * self.n_candidates


    def bullet_voting(self):
        if self.selected_scheme == 0:
            print("Bullet Voting for Plurality scheme not possible.")
            return False
        

        for candidate_index, candidate in enumerate(range(self.n_candidates)):

            happiness_vector = self.votingrunner.calculate_voters_happiness(self.preference_matrix, self.voting_outcome)
            overall_happiness = self.votingrunner.calculate_overall_happiness(happiness_vector)
            candidate_happiness = happiness_vector[candidate_index]

       

            for preference in np.unique(self.preference_matrix):

                bullet_preference_matrix = np.copy(self.preference_matrix)
                bullet_preference_matrix[1:, candidate] = 0
                bullet_preference_matrix[0, candidate] = preference

                strategic_voting_results = self.votingrunner.run_voting_simulation(bullet_preference_matrix, self.selected_scheme)
                del strategic_voting_results[0]

                happiness_tactical = self.votingrunner.calculate_voters_happiness(self.preference_matrix, strategic_voting_results)
                overall_happiness_tactical = self.votingrunner.calculate_overall_happiness(happiness_tactical)
                candidate_happiness_tactical = happiness_tactical[candidate_index]

                if candidate_happiness_tactical > candidate_happiness:
                    self.strategic_voting_options[candidate_index] = [bullet_preference_matrix, strategic_voting_results, overall_happiness_tactical, "Happiness is increased for voter by : {}".format(candidate_happiness_tactical - candidate_happiness)]
                
        return True

    def compromising_strategy(self, preference_matrix, voting_outcome):
        self.vh1 = self.votingrunner.calculate_voters_happiness(preference_matrix, voting_outcome)
        self.newpref = [[]] * len(preference_matrix[0])

        for i in range(len(preference_matrix[0])):
            for j in range(len(preference_matrix[:,0])):
                for k in range(len(preference_matrix[:,0])):
                    if k != j:
                        self.pref2 = deepcopy(preference_matrix)
                        tmp = self.pref2[j,i]
                        self.pref2[j,i] = self.pref2[k,i]
                        self.pref2[k,i] = tmp
                        self.vh2 = self.votingrunner.calculate_voters_happiness(self.pref2, voting_outcome)
                        #print("\nInit VH : {}, new VH: {}".format(self.vh1,self.vh2))
                        if (self.vh1[i] < self.vh2[i]):
                            self.newpref[i] = deepcopy(self.pref2)
                        # if (calculate happiness>): pref2 = modified_preference_matrix
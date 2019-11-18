from voting_schemes_runner import VotingSchemesRunner
from itertools import chain, permutations, combinations
from sympy.utilities.iterables import multiset_permutations
from copy import copy, deepcopy

class TacticalVoting:
    def __init__(self, preference_matrix, voting_outcome, selected_scheme):
        self.preference_matrix = preference_matrix
        self.voting_outcome = voting_outcome
        self.votingrunner = VotingSchemesRunner()
        self.selected_scheme = selected_scheme

    def bullet_voting(self):
        pass

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
import numpy as np
from collections import OrderedDict

class VotingSchemesRunner:
    def __init__(self):
        pass

    def run_voting_simulation(self, preference_matrix, voting_scheme):
        preference_matrix = np.array(preference_matrix, dtype=np.uint8)
        # Select Voting Schemes to Run
        if voting_scheme == 0:
            return self.plurality_voting(preference_matrix)
        elif voting_scheme == 1:
            return self.voting_for_two(preference_matrix)
        elif voting_scheme == 2:
            return self.anti_plurality_voting(preference_matrix)
        elif voting_scheme == 3:
            return self.borda_voting(preference_matrix)    


    def calculate_voter_happiness(self):
        pass
    
    def calculate_overall_happiness(self, vector_happiness):
        self.overall_happiness = np.sum(vector_happiness)
        print("\nOverall Happiness of population is: {}".format(self.overall_happiness))

    def plurality_voting(self, preference_matrix):
        preferences = {k: 0 for k in preference_matrix[:, 0]}
        print(preferences)
        unique, counts = np.unique(preference_matrix[0, :], return_counts=True)
        for index, element in enumerate(unique):
            preferences[element] += counts[index]
        
        return dict(sorted(preferences.items(), key= lambda x:x[1], reverse=True))

    def voting_for_two(self, preference_matrix):
        """Check for most frequently mentioned preferences in first two columns"""

        preferences = {k:0 for k in preference_matrix[:, 0]}

        for i in range(2):
            unique, counts = np.unique(preference_matrix[i, :], return_counts=True)
            for index, element in enumerate(unique):
                preferences[element] += counts[index]

        return dict(sorted(preferences.items(), key= lambda x:x[1], reverse=True))


    def anti_plurality_voting(self, preference_matrix):
        preferences = {k:0 for k in preference_matrix[:, 0]}

        # TODO: check if the one with most votes really wins
        n_candidates = preference_matrix.shape[0]
        for i in range(n_candidates):
            unique, counts = np.unique(preference_matrix[i, :], return_counts=True)
            for index, element in enumerate(unique):
                preferences[element] += counts[index]

        return dict(sorted(preferences.items(), key= lambda x:x[1], reverse=True))


    def borda_voting(self, preference_matrix):
        preferences = {k:0 for k in preference_matrix[:, 0]}
        n_candidates = preference_matrix.shape[0]
        for i in range(n_candidates):
            borda_factor = n_candidates - i - 1
            unique, counts = np.unique(preference_matrix[i, :], return_counts=True)
            for index, element in enumerate(unique):
                preferences[element] += counts[index] * borda_factor

        return dict(sorted(preferences.items(), key= lambda x:x[1], reverse=True))

        
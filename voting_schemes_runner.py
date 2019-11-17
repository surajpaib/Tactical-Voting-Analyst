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


    def calculate_voters_happiness(self, preference_matrix, voting_outcome):
        vector_happiness = []
        for voter_preference_list in preference_matrix.T:
            d = 0
            for j in range(len(voter_preference_list)):
                candidate = voter_preference_list[j]
                k = list(voting_outcome).index(candidate)  # position of the candidate in the voting outcome 
                weight = j+1   # j starts at 0 but we want weight to start at 1
                d += weight * (k-j)
            voter_happiness = 1 / (1 + abs(d))
            vector_happiness.append(voter_happiness)
        return np.array(vector_happiness)
        
    def calculate_overall_happiness(self, vector_happiness):
        self.overall_happiness = np.sum(vector_happiness)
        return self.overall_happiness

    def plurality_voting(self, preference_matrix):
        preferences = {k:0 for k in np.unique(preference_matrix)}
        print(preferences)
        unique, counts = np.unique(preference_matrix[0, :], return_counts=True)
        for index, element in enumerate(unique):
            preferences[element] += counts[index]
        
        return dict(sorted(preferences.items(), key= lambda x:x[1], reverse=True))

    def voting_for_two(self, preference_matrix):
        """Check for most frequently mentioned preferences in first two columns"""

        preferences = {k:0 for k in np.unique(preference_matrix)}

        for i in range(2):
            unique, counts = np.unique(preference_matrix[i, :], return_counts=True)
            for index, element in enumerate(unique):
                preferences[element] += counts[index]

        return dict(sorted(preferences.items(), key= lambda x:x[1], reverse=True))


    def anti_plurality_voting(self, preference_matrix):
        preferences = {k:0 for k in np.unique(preference_matrix)}

        # TODO: check if the one with most votes really wins
        n_preferences = preference_matrix.shape[0]
        for i in range(n_preferences-1):
            unique, counts = np.unique(preference_matrix[i, :], return_counts=True)
            for index, element in enumerate(unique):
                preferences[element] += counts[index]

        return dict(sorted(preferences.items(), key= lambda x:x[1], reverse=True))


    def borda_voting(self, preference_matrix):
        preferences = {k:0 for k in np.unique(preference_matrix)}
        n_preferences = preference_matrix.shape[0]
        for i in range(n_preferences):
            borda_factor = n_preferences - i - 1
            unique, counts = np.unique(preference_matrix[i, :], return_counts=True)
            for index, element in enumerate(unique):
                preferences[element] += counts[index] * borda_factor

        return dict(sorted(preferences.items(), key= lambda x:x[1], reverse=True))

        
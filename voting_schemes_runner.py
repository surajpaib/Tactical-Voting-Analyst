import numpy as np
from collections import OrderedDict

class VotingSchemesRunner:
    def __init__(self):
        self.results = None

    def voting_simulation(self, preference_matrix, voting_scheme):
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

    def get_happiness(self, preference_matrix, voting_outcome: OrderedDict):
        """calculate happiness for each voter"""
        vector_happiness = []
        for voter_preference_list in preference_matrix.T:
            d = 0
            pref_len = len(voter_preference_list)
            for i in range(pref_len):
                j =  pref_len - i  # position of the candidate in the true preference list
                candidate = voter_preference_list[i]
                k = pref_len - list(voting_outcome).index(candidate)  # position of the candidate in the voting outcome
                d += j*(k-j)
            voter_happiness = 1 / (1 + abs(d))
            vector_happiness.append(voter_happiness)
        return np.array(vector_happiness)
        
    def plurality_voting(self, preference_matrix):
        preferences = {k:0 for k in np.unique(preference_matrix)}
        unique, counts = np.unique(preference_matrix[0, :], return_counts=True)
        for index, element in enumerate(unique):
            preferences[element] += counts[index]
        self.results = dict(sorted(preferences.items(), key= lambda x:x[1], reverse=True))
        return self.results

    def voting_for_two(self, preference_matrix):
        """Check for most frequently mentioned preferences in first two columns"""
        preferences = {k: 0 for k in np.unique(preference_matrix)}
        for i in range(2):
            unique, counts = np.unique(preference_matrix[i, :], return_counts=True)
            for index, element in enumerate(unique):
                preferences[element] += counts[index]
        self.results = dict(sorted(preferences.items(), key= lambda x:x[1], reverse=True))
        return self.results

    def anti_plurality_voting(self, preference_matrix):
        preferences = {k:0 for k in np.unique(preference_matrix)}

        # TODO: check if the one with most votes really wins
        n_preferences = preference_matrix.shape[0]
        for i in range(n_preferences-1):
            unique, counts = np.unique(preference_matrix[i, :], return_counts=True)
            for index, element in enumerate(unique):
                preferences[element] += counts[index]
        self.results = dict(sorted(preferences.items(), key= lambda x:x[1], reverse=True))
        return self.results

    def borda_voting(self, preference_matrix):
        preferences = {k:0 for k in np.unique(preference_matrix)}
        n_preferences = preference_matrix.shape[0]
        for i in range(n_preferences):
            borda_factor = n_preferences - i - 1
            unique, counts = np.unique(preference_matrix[i, :], return_counts=True)
            for index, element in enumerate(unique):
                preferences[element] += counts[index] * borda_factor
        self.results = dict(sorted(preferences.items(), key= lambda x:x[1], reverse=True))
        return self.results

        
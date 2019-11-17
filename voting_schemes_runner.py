import numpy as np


class VotingSchemesRunner:
    def __init__(self, preference_matrix, voting_scheme):
        self.preference_matrix = np.array(preference_matrix, dtype=np.uint8)
        self.voting_scheme = voting_scheme

        # Select Voting Schemes to Run
        if self.voting_scheme == 0:
            self.plurality_voting(self.preference_matrix)
        elif self.voting_scheme == 1:
            self.voting_for_two(self.preference_matrix)
        elif self.voting_scheme == 2:
            self.anti_plurality_voting(self.preference_matrix)
        elif self.voting_scheme == 3:
            self.borda_voting(self.preference_matrix)    

    def calculate_voter_happiness(self):
        pass

    def plurality_voting(self, preference_matrix):
        unique, counts = np.unique(preference_matrix[0, :], return_counts=True)
        print(unique, counts)
        self.voting_outcome = unique[np.argmax(counts)]
        print("\nNon-Strategic Voting Outcome is: {}".format(chr(self.voting_outcome)))

    def voting_for_two(self, preference_matrix):
        preferences = {}
        for i in range(2):
            unique, counts = np.unique(preference_matrix[i, :], return_counts=True)
            for index, element in enumerate(unique):
                if element not in preferences:
                    preferences[element] = counts[index]
                else:
                    preferences[element] += counts[index]

        
        self.voting_outcome = max(preferences, key=preferences.get)
        print("\nNon-Strategic Voting Outcome is: {}".format(chr(self.voting_outcome)))


    def anti_plurality_voting(self, preference_matrix):
        preferences = {}
        for i in range(len(preference_matrix[:, 0])):
            unique, counts = np.unique(preference_matrix[i, :], return_counts=True)
            for index, element in enumerate(unique):
                if element not in preferences:
                    preferences[element] = counts[index]
                else:
                    preferences[element] += counts[index]

        print(preferences)
        self.voting_outcome = max(preferences, key=preferences.get)
        print("\nNon-Strategic Voting Outcome is: {}".format(chr(self.voting_outcome)))


    def borda_voting(self, preference_matrix):
        preferences = {}
        for i in range(len(preference_matrix[:, 0])):
            borda_factor = len(preference_matrix[:, 0]) - i - 1
            unique, counts = np.unique(preference_matrix[i, :], return_counts=True)
            for index, element in enumerate(unique):
                if element not in preferences:
                    preferences[element] = counts[index] * borda_factor
                else:
                    preferences[element] += counts[index] * borda_factor

        print(preferences)
        self.voting_outcome = max(preferences, key=preferences.get)
        print("\nNon-Strategic Voting Outcome is: {}".format(chr(self.voting_outcome)))

        
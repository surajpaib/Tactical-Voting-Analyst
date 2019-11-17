from voting_schemes_runner import VotingSchemesRunner
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
            bullet_preference_matrix = np.copy(self.preference_matrix)
            bullet_preference_matrix[1:, candidate] = 0
            print("Candidate Matrix: {}".format(bullet_preference_matrix))
            strategic_voting_results = self.votingrunner.run_voting_simulation(bullet_preference_matrix, self.selected_scheme)
            del strategic_voting_results[0]
            self.strategic_voting_options[candidate_index] = strategic_voting_results
        
        return True

    def compromising_strategy(self):
        pass
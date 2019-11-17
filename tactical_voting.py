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

            happiness_vector = self.votingrunner.calculate_voters_happiness(self.preference_matrix, self.voting_outcome)
            overall_happiness = self.votingrunner.calculate_overall_happiness(happiness_vector)
            candidate_happiness = happiness_vector[candidate_index]

            bullet_preference_matrix = np.copy(self.preference_matrix)
            bullet_preference_matrix[1:, candidate] = 0

            for preference in np.unique(self.preference_matrix):
                bullet_preference_matrix[0, candidate] = preference
                print("Candidate Matrix: {}".format(bullet_preference_matrix))
                strategic_voting_results = self.votingrunner.run_voting_simulation(bullet_preference_matrix, self.selected_scheme)
                del strategic_voting_results[0]

                happiness_tactical = self.votingrunner.calculate_voters_happiness(self.preference_matrix, strategic_voting_results)
                overall_happiness_tactical = self.votingrunner.calculate_overall_happiness(happiness_tactical)
                candidate_happiness_tactical = happiness_tactical[candidate_index]

                if candidate_happiness_tactical > candidate_happiness:
                    self.strategic_voting_options[candidate_index] = [bullet_preference_matrix, strategic_voting_results, overall_happiness_tactical, "Happiness is increased for voter by : {}".format(candidate_happiness_tactical - candidate_happiness)]
                
        return True

    def compromising_strategy(self):
        pass
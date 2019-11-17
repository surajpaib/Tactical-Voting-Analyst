from voting_schemes_runner import VotingSchemesRunner

class TacticalVoting:
    def __init__(self, preference_matrix, voting_outcome, selected_scheme):
        self.preference_matrix = preference_matrix
        self.voting_outcome = voting_outcome
        self.votingrunner = VotingSchemesRunner()
        self.selected_scheme = selected_scheme

    def bullet_voting(self):
        pass

    def compromising_strategy(self):
        pass
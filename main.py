from preference_creator import PreferenceCreator
from voting_schemes_runner import VotingSchemesRunner

if __name__ == "__main__":
    preference_creator = PreferenceCreator()
    preference_matrix, selected_scheme = preference_creator.get_preferences()
    votingrunner = VotingSchemesRunner(preference_matrix, selected_scheme)
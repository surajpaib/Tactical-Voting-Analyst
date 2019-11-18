from preference_creator import PreferenceCreator
from voting_schemes_runner import VotingSchemesRunner
from tactical_voting import TacticalVoting

if __name__ == "__main__":
    preference_creator = PreferenceCreator()
    preference_matrix, selected_scheme = preference_creator.get_preferences()
    votingrunner = VotingSchemesRunner()
    strategic_voting_results = votingrunner.run_voting_simulation(preference_matrix, selected_scheme)
    tactical_voting = TacticalVoting(preference_matrix, strategic_voting_results, selected_scheme)
    tactical_voting.compromising_strategy(preference_matrix, strategic_voting_results)
    print("Strategic Voting Results: {}".format(strategic_voting_results))      
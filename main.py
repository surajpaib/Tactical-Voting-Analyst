from preference_creator import PreferenceCreator
from voting_schemes_runner import VotingSchemesRunner
from tactical_voting import TacticalVoting

if __name__ == "__main__":
    preference_creator = PreferenceCreator()
    preference_matrix, selected_scheme = preference_creator.get_preferences()
    votingrunner = VotingSchemesRunner()
    #tactical_voting = TacticalVoting(preference_matrix, strategic_voting_results, selected_scheme)
    #tactical_voting.compromising_strategy(preference_matrix, strategic_voting_results)
    voting_results = votingrunner.run_voting_simulation(preference_matrix, selected_scheme)
    print("Voting Results: {}".format(voting_results))          
    tactical_voter = TacticalVoting(preference_matrix, voting_results, selected_scheme)
    if tactical_voter.bullet_voting():
        for candidate_options in tactical_voter.strategic_voting_options:
            print("Options for candidate: {}\n".format(candidate_options))

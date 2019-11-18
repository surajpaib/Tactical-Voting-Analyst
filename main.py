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
            
            
    compromise_results = tactical_voter.compromising_strategy(preference_matrix, voting_results)
    
    for candidate in range(len(preference_matrix[0])):
        print("\nCandidate {}:\n>Original Pref List: {}; Original Happiness Vector: {};".format(
                candidate+1,
                preference_matrix[:,candidate],
                votingrunner.calculate_voters_happiness(preference_matrix, voting_results)))        
        print("\n>Modified preference matrix for candidate {} using compromise/burrying:\n {}".format(candidate+1, compromise_results[candidate]))
        if len(compromise_results[candidate])>0:
            print("\n>>New happiness vector:\n>>{}".format(
                    votingrunner.calculate_voters_happiness(
                            compromise_results[candidate],
                            votingrunner.run_voting_simulation(compromise_results[candidate],selected_scheme)
                        )
                    ))

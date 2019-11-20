from preference_creator import PreferenceCreator as PC
from voting_schemes_runner import VotingSchemesRunner as VSR
from tactical_voting import TacticalVoting

if __name__ == "__main__":
    pc = PC()
    vsr = VSR()
    pref_mat, scheme = pc.get_preferences()
    #tactical_voting = TacticalVoting(pref_mat, strategic_voting_results, scheme)
    #tactical_voting.compromising_strategy(pref_mat, strategic_voting_results)
    voting_results = vsr.voting_simulation(pref_mat, scheme)
    print("Voting Results: {}\n".format(voting_results))          
    tactical_voter = TacticalVoting(pref_mat, voting_results, scheme)
    if tactical_voter.bullet_voting():
        for candidate_options in tactical_voter.strategic_voting_options:
            print("Options for candidate: {}\n".format(candidate_options))
            
            
    compromise_results = tactical_voter.compromising_strategy(pref_mat, voting_results)
    
    for candidate in range(len(pref_mat[0])):
        print("\nCandidate {}:\n>Original Pref List: {}; Original Happiness Vector: {};".format(
                candidate+1,
                pref_mat[:,candidate],
                vsr.get_happiness(pref_mat, voting_results)))        
        print("\n>Modified preference matrix for candidate {} using compromise/burrying:\n {}".format(candidate+1, compromise_results[candidate]))
        if len(compromise_results[candidate])>0:
            print("\n>>New happiness vector:\n>>{}".format(
                    vsr.get_happiness(
                            compromise_results[candidate],
                            vsr.voting_simulation(compromise_results[candidate],scheme)
                        )
                    ))

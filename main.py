from preference_creator import PreferenceCreator as PC
from voting_schemes_runner import VotingSchemesRunner as VSR
from tactical_voting import TacticalVoting
import integration_tests as IT


# TODO: Replace values 65, 66, ... with alphabetical values in output!
if __name__ == "__main__":
    modes = {1: "Manual Input",
             2: "Integration test: 2 candidates, 3 voters, voting for two",
             3: "Integration test: M candidates, N voters, pick a voting scheme"}
    for k, v in modes.items():
        print("{}: {}".format(k, v))
    mode = input("\nPlease choose one of the options listed [1/2/3]\n")
    if mode=="1":
        pc = PC()
        vsr = VSR()
        pc.get_preferences()
        vsr.voting_simulation(pc.pref_mat, pc.scheme)
        tv = TacticalVoting(pc.pref_mat, vsr.results, pc.scheme)
    elif mode=="2":
        pc, vsr, tv = IT.integration_voting_for_two()
    elif mode=="3":
        M = int(input("Enter number of candidates: "))
        if not(isinstance(M, int)) or (not M>0): 
            print("Select an Integer > 0")
            exit()
        N = int(input("Enter number of voters: "))
        if not(isinstance(N, int)) or (not N>0): 
            print("Select an Integer > 0")
            exit()
        voting_schemes = ['1: Plurality Voting', '2: Voting for two', '3: Anti-Plurality Voting', '4: Borda Voting']
        scheme = int(input("Select the Voting Scheme using the indexes \n{}:".format(voting_schemes))) - 1
        if scheme > 3 or scheme < 0:
            print("\n Select a value between 1 and 4")
            exit()
        pc, vsr, tv = IT.integration_MxN(M, N, scheme)
    else:
        print("Invalid Input")
        exit()

    print("\nPreference matrix:\n{}".format(pc.pref_mat))    

    # Non-strategic voting
    overall_happiness = sum(vsr.get_happiness(pc.pref_mat, vsr.results))
    print("\nNon-strategic voting outcome: {}".format(vsr.results))
    print("Overall voter happiness level: {}".format(overall_happiness))

    # Bullet voting
    tv.bullet_voting()       

    # Compromising / Burying            
    tv.compromising_strategy()

    for i, options in enumerate(tv.strategic_voting_options):
        print("\nOptions for voter {}:".format(i))
        for option in options:
            for k, v in option.items():
                print("\t{}\t: {}".format(k, v))
            print()

    strat_voting_risk = sum(len(i) for i in tv.strategic_voting_options) / pc.num_voters
    print("\nOverall risk of strategic voting: {}".format(strat_voting_risk))

    # for candidate in range(len(pc.pref_mat[0])):
    #     print("\nCandidate {}:\n>Original Pref List: {}; Original Happiness Vector: {};".format(
    #             candidate+1,
    #             pc.pref_mat[:,candidate],
    #             vsr.get_happiness(pc.pref_mat, vsr.results)))        
    #     print("\n>Modified preference matrix for candidate {} using compromise/burrying:\n {}".format(candidate+1, compromise_results[candidate]))
    #     if len(compromise_results[candidate])>0:
    #         print("\n>>New happiness vector:\n>>{}".format(
    #                 vsr.get_happiness(
    #                         compromise_results[candidate],
    #                         vsr.voting_simulation(compromise_results[candidate],pc.scheme)
    #                     )
    #                 ))

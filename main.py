from preference_creator import PreferenceCreator as PC
from voting_schemes_runner import VotingSchemesRunner as VSR
from tactical_voting import TacticalVoting
import integration_tests as IT


if __name__ == "__main__":
    modes = {1: "Manual input",
             2: "Integration test: 2 candidates, 3 voters, voting for two",
             3: "Integration test: M candidates, N voters, pick a voting scheme, random preferences"}
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
    str_pref_mat = [[chr(j) for j in i] for i in pc.pref_mat]
    print("\nPreference matrix:")
    for i in str_pref_mat:
        print(i)

    # Non-strategic voting
    overall_happiness = sum(vsr.get_happiness(pc.pref_mat, vsr.results))
    str_results = dict(zip([chr(i) for i in vsr.results.keys()], vsr.results.values()))
    print("\nNon-strategic voting outcome: {}".format(str_results))
    print("Overall voter happiness level: {}".format(overall_happiness))

    # Bullet voting
    tv.bullet_voting()       

    # Compromising / Burying            
    tv.compromising_strategy()

    for i, options in enumerate(tv.strategic_voting_options):
        voter_num = i+1
        print("\nOptions for voter {}:".format(voter_num))
        for option in options:
            for k, v in option.items():
                print("\t{}\t: {}".format(k, v))
            print()

    strat_voting_risk = sum([1 if len(i)>0 else 0 for i in tv.strategic_voting_options]) / pc.num_voters
    print("\nOverall risk of strategic voting: {}".format(strat_voting_risk))

    input("\n\nPress ENTER to leave")

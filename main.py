from preference_creator import PreferenceCreator as PC
from voting_schemes_runner import VotingSchemesRunner as VSR
from tactical_voting import TacticalVoting
import integration_tests as IT

if __name__ == "__main__":
    print({1: "Manual Input",
           2: "Integration Test"})
    mode = input("Please choose one of the options listed [1/2]\n")
    if mode=="1":
        pc = PC()
        vsr = VSR()
        pc.get_preferences()
        vsr.voting_simulation(pc.pref_mat, pc.scheme)
        tv = TacticalVoting(pc.pref_mat, vsr.results, pc.scheme)
    elif mode=="2":
        pc, vsr, tv = IT.integration_voting_for_two()
    else:
        print("Invalid Input")

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
        for j in options:
            print(j)
    
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

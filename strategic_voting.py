import numpy as np
import logging 

class PreferenceCreator:
    def __init__(self):
        pass

    def get_preferences(self):
        self.get_number_of_voters()
        self.get_number_of_candidates()
        self.get_voting_schemes()
        self.preference_matrix = np.zeros((self.number_of_candidates, self.number_of_voters))
        self.list_of_candidates = [chr(65 + offset) for offset in range(self.number_of_candidates)]
    
        print("\n Preference Matrix: \n{}".format(self.preference_matrix))
        print("\n Generated List of Candidates: {}".format(self.list_of_candidates))
        self.get_voter_candidates()
        return self.preference_matrix, self.selected_scheme
        

    def get_voting_schemes(self):
        voting_schemes = ['1: Plurality Voting', '2: Voting for two', '3: Anti-Plurality Voting', '4: Borda Voting']
        while True:
            try: 
                self.selected_scheme = int(input("Select the Voting Scheme using the indexes \n{} :".format(voting_schemes))) - 1
                if self.selected_scheme > 3 or self.selected_scheme < 0:
                    print("\n Select a value between 1 - 4")
                    continue
                else:
                    break
            except:
                print("\nInvalid Scheme selection. Select a value between 1-4")

    def get_voter_candidates(self):
        for voter_number in range(self.number_of_voters):
            print("\n Entering Preferences for Voter {} ".format(voter_number+ 1))
            print("\n Possible options are: {}".format(self.list_of_candidates))
            voter_choices = []
            for candidate_number in range(len(self.list_of_candidates)):
                while True:
                    preference = input("Enter the {} Preference Candidate for Voter {}: ".format(candidate_number+1, voter_number+1))
                    if (preference in self.list_of_candidates and preference not in voter_choices):
                        voter_choices.append(preference)
                        break
                    else:
                        print("The preference selected is invalid or already chosen. Please choose wisely.")
            
            numerical_voter_choices = np.array([int(ord(val)) for val in voter_choices])
            self.preference_matrix[:, voter_number] = numerical_voter_choices
        print("\n Preference Matrix: \n{}".format(self.preference_matrix))
            
                

    def get_number_of_voters(self):
        while True:
            try: 
                self.number_of_voters = int(input("Enter the number of Voters: "))
                break
            except:
                logging.error("Input value for number of voters is incorrect. Please Enter an Integer value")

    def get_number_of_candidates(self):
        while True:
            try: 
                self.number_of_candidates = int(input("\nEnter the number of Candidates: "))
                if self.number_of_candidates > 26:
                    logging.error("Number of Candidates cannot be a value above 26")
                    continue
                break
            except:
                logging.error("Input value for number of Candidates is incorrect. Please Enter an Integer value")


class VotingSchemesRunner:
    def __init__(self, preference_matrix, voting_scheme):
        self.preference_matrix = np.array(preference_matrix, dtype=np.uint8)
        self.voting_scheme = voting_scheme

        # Select Voting Schemes to Run
        if self.voting_scheme == 0:
            self.plurality_voting(self.preference_matrix)
        elif self.voting_scheme == 1:
            self.voting_for_two(self.preference_matrix)
        elif self.voting_scheme == 2:
            self.anti_plurality_voting(self.preference_matrix)
        elif self.voting_scheme == 3:
            self.borda_voting(self.preference_matrix)    

    def calculate_voter_happiness(self):
        pass

    def plurality_voting(self, preference_matrix):
        unique, counts = np.unique(preference_matrix[0, :], return_counts=True)
        print(unique, counts)
        self.voting_outcome = unique[np.argmax(counts)]
        print("\nNon-Strategic Voting Outcome is: {}".format(chr(self.voting_outcome)))

    def voting_for_two(self, preference_matrix):
        preferences = {}
        for i in range(2):
            unique, counts = np.unique(preference_matrix[i, :], return_counts=True)
            for index, element in enumerate(unique):
                if element not in preferences:
                    preferences[element] = counts[index]
                else:
                    preferences[element] += counts[index]

        
        self.voting_outcome = max(preferences, key=preferences.get)
        print("\nNon-Strategic Voting Outcome is: {}".format(chr(self.voting_outcome)))


    def anti_plurality_voting(self, preference_matrix):
        preferences = {}
        for i in range(len(preference_matrix[:, 0])):
            unique, counts = np.unique(preference_matrix[i, :], return_counts=True)
            for index, element in enumerate(unique):
                if element not in preferences:
                    preferences[element] = counts[index]
                else:
                    preferences[element] += counts[index]

        print(preferences)
        self.voting_outcome = max(preferences, key=preferences.get)
        print("\nNon-Strategic Voting Outcome is: {}".format(chr(self.voting_outcome)))


    def borda_voting(self, preference_matrix):
        preferences = {}
        for i in range(len(preference_matrix[:, 0])):
            borda_factor = len(preference_matrix[:, 0]) - i - 1
            unique, counts = np.unique(preference_matrix[i, :], return_counts=True)
            for index, element in enumerate(unique):
                if element not in preferences:
                    preferences[element] = counts[index] * borda_factor
                else:
                    preferences[element] += counts[index] * borda_factor

        print(preferences)
        self.voting_outcome = max(preferences, key=preferences.get)
        print("\nNon-Strategic Voting Outcome is: {}".format(chr(self.voting_outcome)))

        


if __name__ == "__main__":
    preference_creator = PreferenceCreator()
    preference_matrix, selected_scheme = preference_creator.get_preferences()
    votingrunner = VotingSchemesRunner(preference_matrix, selected_scheme)
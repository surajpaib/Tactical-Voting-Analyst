import numpy as np
import logging


class PreferenceCreator:
    def __init__(self):
        self.number_of_voters = 0
        self.number_of_candidates = 0
        self.list_of_candidates = []
        self.preference_matrix = np.array([])
        self.selected_scheme = None

    def get_preferences(self):
        self.get_number_of_voters()
        self.get_number_of_candidates()
        self.get_voting_schemes()
        self.get_voter_candidates()
        return self.preference_matrix, self.selected_scheme
        

    def get_voting_schemes(self):
        voting_schemes = ['1: Plurality Voting', '2: Voting for two', '3: Anti-Plurality Voting', '4: Borda Voting']
        while True:
            try: 
                self.selected_scheme = int(input("Select the Voting Scheme using the indexes \n{} :".format(voting_schemes))) - 1
                if self.selected_scheme > 3 or self.selected_scheme < 0:
                    print("\n Select a value between 1 and 4")
                    continue
                else:
                    break
            except:
                print("\nInvalid scheme selected. Please select a value between 1-4")
                #raise ValueError

    def get_voter_candidates(self):
        """Get user input for voter preferences"""
        for voter_number in range(self.number_of_voters):
            print("\n Enter preferences for voter {}:".format(voter_number+ 1))
            print("Possible options are: {}".format(self.list_of_candidates))
            voter_choices = []
            for candidate_number in range(len(self.list_of_candidates)):
                while True:
                    preference = input("Enter the {}. preferred candidate for voter {}: ".format(candidate_number+1, voter_number+1))
                    if (preference in self.list_of_candidates and preference not in voter_choices):
                        voter_choices.append(preference)
                        break
                    else:
                        print("The preference selected is invalid or already chosen. Please choose wisely.")
            # assign ASCII character values to preferences
            numerical_voter_choices = np.array([int(ord(val)) for val in voter_choices])
            self.preference_matrix[:, voter_number] = numerical_voter_choices
        print("\n Preference Matrix: \n{}".format(self.preference_matrix))
            
                

    def get_number_of_voters(self):
        """ask user for number of voters"""
        while True:
            try: 
                self.number_of_voters = int(input("Enter the number of Voters: "))
                break
            except:
                logging.error("Input value for number of voters is incorrect. Please enter an integer value")
                raise ValueError

    def get_number_of_candidates(self):
        """ask user for number of candidates (up to 26)"""
        while True:
            try: 
                self.number_of_candidates = int(input("\nEnter the number of candidates: "))
                if self.number_of_candidates > 26:
                    logging.error("Number of Candidates cannot be a value above 26")
                    continue
                break
            except:
                logging.error("Input value for number of candidates is incorrect. Please enter an integer value.")
                raise ValueError
        
        # TODO Generalize to unlimited candidates
        self.list_of_candidates = [chr(65 + offset) for offset in range(self.number_of_candidates)]
        self.preference_matrix = np.zeros((self.number_of_candidates, self.number_of_voters))
        print("\n Preference Matrix: \n{}".format(self.preference_matrix))  
        print("\n Generated List of Candidates: {}".format(self.list_of_candidates))


import numpy as np
import logging


class PreferenceCreator:
    def __init__(self, num_voters=0, num_candidates=0, candidate_list=[], pref_mat=np.array([], dtype=np.uint8), scheme=None):
        self.num_voters = num_voters
        self.num_candidates = num_candidates
        self.candidate_list = candidate_list
        self.pref_mat = pref_mat
        self.scheme = scheme

    def get_preferences(self):
        self.get_num_voters()
        self.get_num_candidates()
        self.get_voting_schemes()
        self.get_voter_candidates()

    def get_voting_schemes(self):
        voting_schemes = ['1: Plurality Voting', '2: Voting for two', '3: Anti-Plurality Voting', '4: Borda Voting']
        while True:
            try: 
                self.scheme = int(input("Select the Voting Scheme using the indexes \n{}:".format(voting_schemes))) - 1
                if self.scheme > 3 or self.scheme < 0:
                    print("\n Select a value between 1 and 4")
                    continue
                else:
                    break
            except:
                print("\nInvalid scheme selected. Please select a value between 1-4")
                #raise ValueError

    def get_voter_candidates(self):
        """Get user input for voter preferences"""
        for voter_number in range(self.num_voters):
            print("\n Enter preferences for voter {}:".format(voter_number+ 1))
            print("Possible options are: {}".format(self.candidate_list))
            voter_choices = []
            for candidate_number in range(len(self.candidate_list)):
                while True:
                    preference = input("Enter the {}. preferred candidate for voter {}: ".format(candidate_number+1, voter_number+1))
                    if (preference in self.candidate_list and preference not in voter_choices):
                        voter_choices.append(preference)
                        break
                    else:
                        print("The preference selected is invalid or already chosen. Please choose wisely.")
            # assign ASCII character values to preferences
            numerical_voter_choices = np.array([ord(val) for val in voter_choices])
            self.pref_mat[:, voter_number] = numerical_voter_choices            
                

    def get_num_voters(self):
        """ask user for number of voters"""
        while True:
            try: 
                self.num_voters = int(input("Enter the number of Voters: "))
                break
            except:
                logging.error("Input value for number of voters is incorrect. Please enter an integer value")
                raise ValueError

    def get_num_candidates(self):
        """ask user for number of candidates (up to 26)"""
        while True:
            try: 
                self.num_candidates = int(input("\nEnter the number of candidates: "))
                if self.num_candidates > 26:
                    logging.error("Number of Candidates cannot be a value above 26")
                    continue
                break
            except:
                logging.error("Input value for number of candidates is incorrect. Please enter an integer value.")
                raise ValueError
        
        # TODO Generalize to unlimited candidates
        self.candidate_list = [chr(65 + offset) for offset in range(self.num_candidates)]
        self.pref_mat = np.zeros((self.num_candidates, self.num_voters), dtype=np.uint8)
        print("\n Generated List of Candidates: {}".format(self.candidate_list))


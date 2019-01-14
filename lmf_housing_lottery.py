# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 21:20:27 2018

@author: luisxavierramostormo


LMF HOUSING LOTERY ORACLE

To determine how many points each is worth: multiply importance (how important
the job is for the functioning of the house or how much you hurt others if
you don't do your job) times time commitment.

Example: cooking is 3 hours and importance is 9 (Importance is rated 0-10) then
cooking is worth 27 points (full points)
"""

import random as rd

# multipliers for lateness/omission
MULTIPLIER = {"full": 1,  # done on time or excused and made up
               "late": .5,  # unexcused but, made up (we can use another system for being somewhat late to hourse meeting)
               "miss": 0}  # unexcused, didn't make up || excused but didn't make up

# how critical it is for the functioning of the house, or how much others will suffer if it doesn't get done
IMPORTANCE = {"cooking": 10,
              "meeting": 8,
              "nettoyage": 6,
              "CPW": 7,
              "grand nettoyage": 10} # only one hour

# how long the action takes, in minutes
TIME = {"cooking": 180,
        "meeting": 60,
        "nettoyage": 45,
        "CPW": 60,
        "grand nettoyage": 60}
    
SENIORITY_BOOST = 180*10 # value of a cooking day

        
class Person(object):
    def __init__(self, name, years_at_lmf): # can add attribute to account for getting small room last year
        self.name = name
        self.years_at_lmf = years_at_lmf
        assert years_at_lmf in {0, 1, 2, 3} # at the start of the year
        # we need a table input data. Can be stored in a csv file and manage with pandas
        
    @property
    def score(self):
        return self.deterministic_score()
        
    def deterministic_score(self):
        score = 0
        table = None
        for action in table: # each column is an action that should get done (netoyage, cooking, etc)
            #action is name of column
            #the multiplier of that action is what's stored in the table (if it was on time, late, etc)
            label = None # on name row and action column
            # NOTE: default should be 0 because that's just easy to handle in a spreadsheet
            score += IMPORTANCE[action]*TIME[action]*MULTIPLIER[label]
        return score
    
    def randomized_score(self, mean = 0, var = SENIORITY_BOOST/6):
        # impossible to gain more senior if difference is SENIORITY_SCORE
            # |-> normal distribution, but cut off edges by SENIORITY_SCORE/2
        x = SENIORITY_BOOST # any out of bounds value is the same
        while not (-SENIORITY_BOOST/2 < x < SENIORITY_BOOST/2):
            x = rd.gauss(mean, var)
        return self.score() + x
    
    
def housing_lottery(people):
    """
    Witness needed for run to be official
    """
    results = sorted(people, key = lambda x: x.randomized_score()) # note that key function is called only once in python sort
    return [person.name for person in results]
    


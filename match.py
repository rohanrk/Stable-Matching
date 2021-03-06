import sys
from random import choice

# Default file names if no file names are provided
default_big_filename = "BigListChoices.csv"
default_little_filename = "LittleListChoices.csv"

# Static variables
matches = dict()
matched_littles = set()

""" Function takes in a file names and completes set of all name and preferences dictionary

Assuming csvs are in the following format

big_list:

pledge_name,first_big_choice,second_big_choice,...

little_list:

bro_name,first_little_choice,second_little_choice,...

Make sure there are no spaces between the commas or this will break
"""
def process_file(name):
    all_names = set() # All pledge names or all bros names (who filled ou the form)
    preferences = dict()
    with open(name, mode='r') as f:
        for line in f:
            line = line.strip('\n')
            choices = choices = line.split(",")
            preferences[choices[0]] = choices[1:]
    return preferences    

def match(big_prefs, little_prefs):
    rem_pledges = list(big_prefs.keys())
    # Randomly select pledge. This way duplicates in their lists are handled fairly
    while rem_pledges:
        small = choice(rem_pledges)
        prefs = big_prefs[small]
        rem_pledges.remove(small)
        big, little, little_index = _match(small, prefs, little_prefs, rem_pledges)
        matches[big] = (little, little_index)
            
    return matches
    
"""Helper function that will match a little to their big based on their preferences and 
all bros little preferences

Returns a tuple (matched big, matched little)
"""
def _match(little, prefs, little_prefs, rem_pledges):
    for big in prefs:
        if big in little_prefs:
            little_index = sys.maxsize # Very large number to indiciate that little is not in big's list
            if little in little_prefs[big]:
                little_index = little_prefs[big].index(little)
            if big in matches:
                # Big has already been matched. Check if big prefers this match over their current pairing
                old_little = matches[big][0]
                if little_index < matches[big][1] or (little_index == matches[big][1] and little == choice([little, old_little])):
                    matched_littles.remove(old_little)
                    rem_pledges.append(old_little)
                    matched_littles.add(little)
                    return big, little, little_index
            else:
                matched_littles.add(little)
                return big, little, little_index
        else:
            # Prune the big list of bros who don't want to be bigs
            prefs.remove(big)
    
    # TODO: Pledge has gone through all their preferences and haven't been matched.
    
    
if __name__=='__main__':
    # If you don't specify csv file names we assume your big list is "BigListChoices.csv"
    # and your little list is "LittleListChoices.csv"
    if len(sys.argv) > 3 or len(sys.argv) == 2:
        print("Incorrect number of arguments. Run python3 match.py <bigs_file_name> <littles_file_name>\nif your filenames are titled `BigListChoices.csv` and `LittleListChoices.csv` you can just run python3 match.py")
        sys.exit()
    
    big_prefs = process_file(default_big_filename) if len(sys.argv) == 1 else process_file(sys.argv[1])
    little_prefs = process_file(default_little_filename) if len(sys.argv) == 1 else process_file(sys.argv[2])
    
    
    pairings = match(big_prefs, little_prefs)
    
    # Make sure all littles have bigs
    if not matches or len(matches) != len(big_prefs):
        print("Error: At least one pledge has not received a match.")
        
    # If there's a pairing such that the littles prefer another big and that same big prefers that little, switch up pairings
    
    
    # Finalize by piping lists to outside file. Optional, pipe process to a different file
    with open("results.txt", mode='w') as f:
        print("Results are also written out to `results.txt`")
        for big, little in matches.items():
            out = "Pledge: {} Big: {}".format(little[0], big)
            f.write("{}\n".format(out))
            print(out)
    
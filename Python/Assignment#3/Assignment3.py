""""
Milan Biswakarma
1001430854
Assignment 3
December 15, 2018
"""

"""
https://www.programiz.com/python-programming/methods/list/sort
https://jeffknupp.com/blog/2014/06/18/improve-your-python-python-classes-and-object-oriented-programming/
"""
import pandas as pd
import time

def readfiles():
    # read from the csv file and return a Pandas DataFrame.
    nba = pd.read_csv("1991-2004-nba.dat", delimiter='#')

    # Pandas DataFrame allows you to select columns.
    # We use column selection to split the data.
    # We only need 2 columns in the data file: Player ID and Points.
    columns = ['ID', 'PTS']
    nba_records = nba[columns]

    # For each player, store the player's points in all games in an ordered list.
    # Store all players' sequences in a dictionary.
    pts = {}
    cur_player = 'NULL'
    # The data file is already sorted by player IDs, followed by dates.
    for index, row in nba_records.iterrows():
        player, points = row
        if player != cur_player:
            cur_player = player
            pts[player] = []
        pts[player].append(points)

    return pts

# Streak class for manipulation of the streaks values
class Point:
    def __init__(self, left, right, min, player):
        self.playerID = player  # the player id
        self.left = left        # start index
        self.right = right      # ending index
        self.val = min          # minimum value

    # formats the prominent streaks as desired output
    def formatStreak(self):
        return (self.playerID, self.left, self.getLength(), self.val)
    # gives the length of the string
    def getLength(self):
        return (self.right - self.left + 1)


"""Takes the score, playerID and existing LPS. 
Thens calculate the new LPS or Candidate Streaks for the given sequence of data"""
def LPS_finder(playerID, score, Lps):
    temp_lps = []                   #stores the growing lps to find out the potention LPS

    for i in range(len(score)):
        tracker = None              # tracks the index of the largest streak for v>=k
        lps_delete = []             # keeps the list of the streaks that has to be removed from the growing LPS
        current_score = score[i]    # stores the current score for comparison

        for j in range(len(temp_lps)):
            streak = temp_lps[j]                        # assigns the growing lps streak to varaible streak for calculation

            if (current_score <= streak.val):           # Case I: When v <= k, update growing LPS and store the index for deleting LPS
                lps_delete.append(j)                    # Case I(a):  # Case I: When v < k, update LPS
                if (current_score < streak.val):Lps.append(streak)

                if (tracker is None):                   # If longest index is null then, update
                    tracker = j
                elif (streak.left < temp_lps[tracker].left):
                    tracker = j

            elif (current_score > streak.val):          # Case II: when v > k, update and new growing LPS
                streak.right = i
                continue

        if (tracker is None):                           # for case II : Update the growing LPS
            temp_lps.append(Point(i, i, current_score, playerID))
        else:                                           # for case I : Update the growing LPS
            l = temp_lps[tracker].left
            temp_lps.append(Point(l, i, current_score, playerID))

        for each in sorted(lps_delete, reverse=True):   # sorts and reverses the list to be deleted from growing lps
            temp_lps.pop(each)

    for each in temp_lps:                               # Finally, updated the LPS from the growing LPS
        Lps.append(each)
"""
Takes the candidate points or LPS and input and gives the skyline points.
Uses Liner LPS method and dominance test to find out the skyline points
"""
def SkyLine_finder(candidates):
    ps = []                                             # ps is the prominent streaks or skyline
    for i in range(len(candidates)):
        skyline_delete = []                             # stores the skyline points to be deleted or are dominated
        result = True

        for j in range(len(ps)):

            s1 = candidates[i]
            s2 = ps[j]
            dominance = False
            # the following if-else statement does the check for the dominance for the skyline points
            # it returns 1 for true and -1 for false dominance
            if (s2.getLength() > s1.getLength()) and (s2.val >= s1.val):
                dominance = -1

            elif (s2.getLength() >= s1.getLength()) and (s1.val > s1.val):
                dominance = -1

            elif (s1.getLength() > s2.getLength()) and (s1.val >= s2.val):
                dominance = 1

            elif (s1.getLength() >= s2.getLength()) and (s1.val > s2.val):
                dominance = 1

            if dominance is 1:                              # Case I: Candidate Dominates ; adds it to skyline delete list
                skyline_delete.append(j)
            elif dominance is -1:                           # Case II: prominent streaks dominates; set the result to False
                result = False
                break

        if (result is True):                                # Append the candidates to the prominent streaks
            ps.append(candidates[i])

        for each in sorted(skyline_delete, reverse=True):   # sorts and reverses the skyline to be deleted and pop them out
            ps.pop(each)

    return ps


def prominent_streaks(sequences):

    # list variabe to store all the final formatted prominent streaks
    prominent_streaks = []

    # 1. Find out the candidate streaks for each players
    # Using LPS method
    growing_lps = []
    for player, score in sequences.items():
        LPS_finder(player,score, growing_lps)

    # 2. Find out the skylines points from the candidate streaks
    # Using Linear LPS method to get the prominent streaks
    skylines = SkyLine_finder(growing_lps)

    # 3. Arrange the date in the format( playerId, left, length, value)
    for points in skylines:
        prominent_streaks.append(points.formatStreak())

    # 4. Return the prominent streaks
    return prominent_streaks


t0 = time.time()
sequences = readfiles()
t1 = time.time()
print("Reading the data file takes ", t1 - t0, " seconds.")

t1 = time.time()
streaks = prominent_streaks(sequences)
t2 = time.time()
print("Computing prominent streaks takes ", t2 - t1, " seconds.")
print(streaks)


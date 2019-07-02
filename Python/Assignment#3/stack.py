import pandas as pd
import time


# Data Object for keeping track of streaks
class Streak:
    def __init__(self, start, end, min_val, playerID):
        self.l = start  # start index
        self.r = end  # ending index
        self.v = min_val  # minimum value
        self.playerID = playerID  # the player id

    def getString(self):
        return "<{0}: [{1}, {2}], {3}>".format(self.playerID, self.l, self.r, self.v)

    def getData(self):
        return (self.playerID, self.l, self.getLength(), self.v)

    def getLength(self):
        return self.r - self.l + 1


def dominates(a, b):
    result = 0

    if (a.getLength() > b.getLength()) and (a.v >= b.v):
        result = 1

    elif (a.v > b.v) and (a.getLength() >= b.getLength()):
        result = 1

    elif (b.getLength() > a.getLength()) and (b.v >= a.v):
        result = -1

    elif (b.v > a.v) and (b.getLength() >= a.getLength()):
        result = -1

    return result


def LPS(vals, playerID, lps_streaks):
    streak_list = []

    for i in range(0, len(vals)):

        to_remove = []  # keep track of the streaks we will remove
        max_index = None  # the index of the longest streak with v >= k
        current = vals[i]  # the current data point we're looking at

        for j in range(0, len(streak_list)):
            s = streak_list[j]

            if (s.v < current):
                s.r = i
                continue

            elif (s.v > current):
                lps_streaks.append(s)
                to_remove.append(j)

            else:
                to_remove.append(j)

            if (s.v >= current):
                if (max_index is None):
                    max_index = j
                elif (s.l < streak_list[max_index].l):
                    max_index = j

        if (max_index is None):
            streak_list.append(Streak(i, i, current, playerID))

        else:
            l = streak_list[max_index].l
            streak_list.append(Streak(l, i, current, playerID))

        for item in sorted(to_remove, reverse=True):
            streak_list.pop(item)

    for item in streak_list:
        lps_streaks.append(item)


def Skyline(candidates):
    skylines = []

    for i in range(0, len(candidates)):
        to_remove = []
        result = True

        for j in range(0, len(skylines)):
            dom = dominates(candidates[i], skylines[j])
            if dom is 0:  # Neither dominates
                continue
            elif dom is 1:  # The candidate dominates
                to_remove.append(j)  # We'll remove the fake skyline streak from the list
            elif dom is -1:  # The skyline point dominates
                result = False
                break

        # If the candidate is undominated, add it to the list.
        if result is True:
            skylines.append(candidates[i])

        # If any skyline point was dominated, remove it.
        for index in sorted(to_remove, reverse=True):
            skylines.pop(index)

    return skylines


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


def prominent_streaks(sequences):
    # Your algorithm goes here

    streaks = []  # the data that will be returned

    # First, find the Local Prominent Streaks for each player
    lps_streaks = []
    for player, scores in sequences.items():
        LPS(scores, player, lps_streaks)

    # Next, get the global prominent streaks from the LPS list
    skylines = Skyline(lps_streaks)

    # Correctly format the prominent streak objects' data into a list.
    for s in skylines:
        streaks.append(s.getData())

    # Return the list of prominent streaks
    return streaks

    # You have the freedom to define any other functions that you deem necessary.


t0 = time.time()
sequences = readfiles()
t1 = time.time()
print("Reading the data file takes ", t1 - t0, " seconds.")

t1 = time.time()
streaks = prominent_streaks(sequences)
t2 = time.time()
print("Computing prominent streaks takes ", t2 - t1, " seconds.")
print(streaks)

print("Length of Streak:", len(streaks))
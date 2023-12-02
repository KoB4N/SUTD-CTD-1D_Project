from libdw import pyrebase
from time import time


dburl = "https://ctd-1d-2048-default-rtdb.asia-southeast1.firebasedatabase.app/"
email = "2048@puzzle.com"
password = "2048dabest"
apikey = " AIzaSyAZYShsrvtqiNCUZU5FIniObGCf1VWGBZc"
authdomain = dburl.replace("https://", "")

config = {
    "apiKey": apikey,
    "authDomain": authdomain,
    "databaseURL": dburl,
}

key_hs = "highScores"
key_ls = "latestScores"
score_index = 1
scoreboard_size = 10


def update_score(username, user_score):

    """Updates the database with the score and player name.
       Adds the score to the latest scores list and boots the oldest score.
       If the score is higher than any of the scores in the high score leaderboard,
       boots the lowest score in the high score leaderboard and inserts the new score."""

    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    user = auth.sign_in_with_email_and_password(email, password)
    db = firebase.database()
    user = auth.refresh(user['refreshToken'])

    # Get the user's score from function call.
    # Encodes the user's name, score and time into a string.
    new_score = "{},{},{}".format(username, str(user_score), time())

    # Check if the user's score is worthy of the leaderboard, from the top down.
    for user_score_i in range(1, scoreboard_size + 1):
        node_hs = db.child(key_hs + str(user_score_i)).get(user['idToken'])
        # Scores in the database are saved in the format playerHighScores:username,user_score,time
        highscore_i = node_hs.val()
        if highscore_i:
            highscore_i_value = int(highscore_i.split(",")[1])
        else:
            highscore_i_value = 0

        next_score = new_score
        if user_score > highscore_i_value:
            # Kick out the lowest score in the list of current scores.
            for j in range(user_score_i, scoreboard_size + 1):
                node_hs_shift = db.child(key_hs + str(j)).get(user['idToken'])
                placeholder_score = node_hs_shift.val()
                db.child(key_hs + str(j)).set(next_score, user['idToken'])
                next_score = placeholder_score
            break

    # Resets the next_score variable to be the previously submitted score.
    next_score = new_score

    # Inserts the score into the scoreboard
    for user_score_i in range(1, scoreboard_size + 1):
        node_ls = db.child(key_ls + str(user_score_i)).get(user['idToken'])
        placeholder_score = node_ls.val()
        db.child(key_ls + str(user_score_i)).set(next_score, user['idToken'])
        next_score = placeholder_score


def fetch_high_scores():

    """Returns a list of lists of the 10 highest scores, from highest to lowest.
       e.g. [['hello', 2000, 1701536578.6759918], ['greetings', 1984, 1801536578.6759918]]"""

    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    user = auth.sign_in_with_email_and_password(email, password)
    db = firebase.database()
    user = auth.refresh(user['refreshToken'])

    highscore_list = []
    for list_index in range(1, scoreboard_size + 1):
        node_hs = db.child(key_hs + str(list_index)).get(user['idToken'])
        if node_hs.val():
            name, score, record_time = node_hs.val().split(",")
            score = int(score)
            record_time = float(record_time)
            highscore_list.append([name, score, record_time])
    return highscore_list


def fetch_latest_scores():
    """Returns a list of lists of the 10 latest scores, from latest to oldest.
       The time is returned as a float value.
       e.g. [['hello', 2000], ['greetings', 1984], ['salutations', 247]"""

    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    user = auth.sign_in_with_email_and_password(email, password)
    db = firebase.database()
    user = auth.refresh(user['refreshToken'])

    latest_scores_list = []
    for list_index in range(1, scoreboard_size + 1):
        node_ls = db.child(key_ls + str(list_index)).get(user['idToken'])
        if node_ls.val():
            name, score, record_time = node_ls.val().split(",")
            score = int(score)
            record_time = float(record_time)
            latest_scores_list.append([name, score, record_time])
    return latest_scores_list

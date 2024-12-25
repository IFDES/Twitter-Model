'''
Title: Track Followers File
authors: Garrick Tse, Eric Mo, Alizain Malik, Ahyan Amin
date-created: 2024-11-15
'''
import sqlite3
from datetime import datetime

def show_tweets(connection, cursor, user_id, offset, limit,start):
    tweets_query = """
    SELECT text, tdate, ttime
    FROM tweets
    where writer_id = ?
    ORDER BY tdate DESC, ttime DESC
    LIMIT ? OFFSET?;
    """

    # Execute the query
    cursor.execute(tweets_query, (user_id, limit, offset))
    tweets = cursor.fetchall()

    # Displaying tweets
    if tweets:
       for i, tweet in enumerate(tweets, start):
            content, date, time = tweet
            print(f"\nTweet {i}")
            print(f"Date: {date} | Time: {time}")
            print(f"Tweet: {content}")
            print("-" * 40)
    else:
        print("There are no more tweets to view.")
  

def follow_user(connection, cursor, flwee_id, host_id):

    # Check if the host is already following the user
    check_query = """
    SELECT 1
    FROM follows
    WHERE flwer = ? AND flwee = ?;
    """
    
    cursor.execute(check_query,(host_id,flwee_id))
    result = cursor.fetchone()

    # Evaluating the result
    if result:
        print("You are already following the User.")
    else:
        insert_query = """
        INSERT INTO follows (flwer, flwee, start_date)
        VALUES (?, ?, ?)
        """
        # Get the current date
        current_date = datetime.today().date()

        # Format the date to YYYY-MM-DD
        formatted_date = current_date.strftime('%Y-%m-%d')

        # Execute and commit changes
        cursor.execute(insert_query,(host_id,flwee_id,formatted_date))
        connection.commit()
        print("You are now following the user.")


def listFollowers(connection, cursor, user_id):
    limit = 5
    offset = 0
    follower_ids = []

    # Main Loop
    while True:

        # Query for the inital 5 followers if applicable
        query = """
        SELECT flwer
        FROM follows
        WHERE flwee = ?
        LIMIT ? OFFSET ?
        """
        cursor.execute(query, (user_id,limit,offset))
        results = cursor.fetchall()

        if not results:
            print("All followers have been presented.")  # In the case of 0 followers or if all followerse have already been shown
        
        # Displaying list of followers
        for item in results:
            follower_id = item[0]
            follower_ids.append(follower_id)
            get_details = """
            SELECT name 
            FROM users
            WHERE usr = ?
            """
            cursor.execute(get_details, (follower_id,))
            name = cursor.fetchall()[0][0]
            print(f"Name: {name}, UserID: {follower_id}")

            
        # Getting user to decide next action
        next_step = input('''
    1. See More Followers
    2. Select A User
    3. Exit
                                                                
    > ''')
        
        if next_step == "1":
            offset += limit
        elif next_step == "2":
            if follower_ids:  # Only give them the opton to select if they have atleast one follower
                check = False
                while not check:
                    selection = int(input("Enter the UserID of your selected User: "))
                    if selection not in follower_ids:
                        print("Please refer to the users listed above.")
                    else:
                        break
                user_info(connection,cursor,selection, user_id)
            else:
                print("You have no followers to select.")
        else:
            break
      

def user_info(connection, cursor, user_id, host_id):

    # Counting number of tweets by selected user
    tweet_query = "SELECT COUNT(*) FROM tweets WHERE writer_id = ?"
    cursor.execute(tweet_query, (user_id,))
    tweet_count = cursor.fetchone()[0]
    print(f"TWEET COUNT: {tweet_count}")

    # Counting number of users being followed by the selected user
    following_query = "SELECT COUNT(*) FROM follows WHERE flwer = ?"
    cursor.execute(following_query, (user_id,))
    following_count = cursor.fetchone()[0]
    print(f"FOLLOWING COUNT: {following_count}")

    # Counting number of users following the selected user
    followers_query = "SELECT COUNT(*) FROM follows WHERE flwee = ?"
    cursor.execute(followers_query, (user_id,))
    followers_count = cursor.fetchone()[0]
    print(f"FOLLOWERS COUNT: {followers_count}")

    # SHOW 3 MOST RECENT TWEETS
    tweet_limit = 3
    tweet_offset = 0
    print_start = 1
    show_tweets(connection, cursor, user_id, tweet_offset, tweet_limit,print_start)

    # Main loop for when they are viewing a selected user
    while True:
        next_step = input('''
    1. See More Tweets
    2. Follow User
    3. Go Back
                                                                
    > ''')
        
        if next_step == "1":
            tweet_offset += tweet_limit
            print_start += tweet_limit
            show_tweets(connection, cursor, user_id, tweet_offset, tweet_limit,print_start)
        elif next_step == "2":
            follow_user(connection, cursor, user_id, host_id)
        else:
            break

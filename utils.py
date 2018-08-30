from dotenv import load_dotenv, find_dotenv
import praw 
import os

load_dotenv(find_dotenv())


def get_reddit_instance(sub_name, user_agent):
	reddit = praw.Reddit(client_id=os.getenv('CLIENT_ID'),
						 client_secret=os.getenv('CLIENT_SECRET'),
						 password=os.getenv('CLIENT_PASSWORD'),
						 username=os.getenv('CLIENT_USERNAME'),
						 user_agent=user_agent)

	subreddit = reddit.subreddit(sub_name)

	bot_name = os.getenv('CLIENT_USERNAME')

	return [subreddit, bot_name]
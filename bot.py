'''
	This is a small reddit bot that replies to people on /r/BokuNoHeroAcademia/
	Resources: 
	https://docs.python.org/3/library/sqlite3.html#module-sqlite3
	https://praw.readthedocs.io/en/latest/
'''

from dotenv import load_dotenv, find_dotenv
from utils import get_reddit_instance
import sqlite3
import praw 
import os
import re

# env variables 

load_dotenv(find_dotenv())


# sqlite3 connection  

db = sqlite3.connect('db.sqlite3')
db_cursor = db.cursor()


# main bot 

LOOKUP_PHRASE = ['this is so sad']

def get_scripted_reply(count):
	return 'nan desu ka? ALEXA, PLAY DESPACITO \n\n *I am a bot and I told alexa to play despacito {x} times*'.format(x=count)


def process_comment(comment):
	'''
		Check if a comment contains the right keywords. 
		If it does, check if it is already in the db (multiple different keywords can be found in the same sentence) 
		If not in the db, save it and reply to it 
	'''
	for phrase in LOOKUP_PHRASE:
		if re.search(phrase, comment.body, re.IGNORECASE):
			query = { 'comment': comment.body, 'created_at': comment.created_utc }

			result = db_cursor.execute("SELECT comment FROM posts WHERE comment=:comment and created_at=:created_at", query).fetchone() 
	
			if result is None:
				# save 
				db_cursor.execute("INSERT INTO posts VALUES (?,?,?)", (comment.submission.id, comment.body, comment.created_utc))
				db.commit()

				# reply 
				number_of_despacitos = len(db_cursor.execute("SELECT * FROM posts").fetchall())
				comment.reply(get_scripted_reply(number_of_despacitos))
				
				# print to console
				print(comment.body)
				print(get_scripted_reply(number_of_despacitos))


def main():	
	subreddit, bot_name = get_reddit_instance('BokuNoHeroAcademia', os.getenv('USER_AGENT'))

	'''
		Up to 100 historical comments will be initially returned
		https://praw.readthedocs.io/en/v4.0.0/code_overview/other/subredditstream.html#praw.models.reddit.subreddit.SubredditStream
	'''

	for comment in subreddit.stream.comments():
		# if a comment is deleted, comment.author returns None and comment.author.name throws AttributeError 
		if comment.author is None:
			continue 

		# do not respond to yourself (in case what you reply with contains your lookup phrase too)
		if comment.author.name != bot_name:
			process_comment(comment)


if __name__ == '__main__':
	main()


# db.close()
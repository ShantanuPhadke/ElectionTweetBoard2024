from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

# For Background Scheduling
import datetime
import logging
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

from electiontweetboard.tokenizers.tokenizer_utils import tokenizer_minify

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])
app.config['SECRET_KEY'] = 'secret_key'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://snwmumshcsdhgd:63d1821b97e3e24111e9d36e496538ea0147c55db5ad52f5a7ed6357a8196c3d@ec2-3-217-146-37.compute-1.amazonaws.com:5432/dv41rc55lk3kl';
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prod.db'
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from electiontweetboard import routes, commands
from electiontweetboard.models import Tweet
# Our TwitterConnection and VaderWrapper Singletons of course
from electiontweetboard.data.TwitterScraper import TwitterScraper
from electiontweetboard.nlp.SentimentAnalyzer import SentimentAnalyzer
from electiontweetboard.locations.LocationManager import LocationManager
from electiontweetboard.politicians.PoliticianManager import PoliticianManager

# Our actual TwitterConnection and VADER Wrapper objects
my_twitter_scraper = TwitterScraper.getInstance()
my_sentiment_analyzer = SentimentAnalyzer.getInstance()
my_location_manager = LocationManager.getInstance()
my_politician_manager = PoliticianManager.getInstance()

def masterGeographicSentimentAnalyzer():
	with app.app_context():
		all_states_info = my_location_manager.getAllStatesInfo()
		all_politicians = my_politician_manager.getPoliticians()
		for politician in all_politicians:
			my_sentiment_analyzer.setQueryTerm(politician)
			for state in all_states_info:
				num_positive = 0.0
				num_negative = 0.0
				num_neutral = 0.0
				for city in all_states_info[state]:
					current_city_info = all_states_info[state][city]
					tweets =  my_twitter_scraper.getTweetsForQuery(politician, 10, current_city_info)
					for tweet in tweets:
						try:
							sentiment = my_sentiment_analyzer.getSentimentForTweet(tweet['text'])
							if sentiment == 'Positive':
								num_positive += 1
							elif sentiment == 'Negative':
								num_negative += 1
							else:
								num_neutral += 1
						except Exception as e:
							continue
				num_total = num_positive + num_negative + num_neutral
				commands.loadStateSentimentDistribution(
					politician, state, (num_negative/num_total)*100, (num_neutral/num_total)*100, (num_positive/num_total)*100
				)
				print('Finished loading ' + politician + "'s sentiments in state " + state)

def getLastProcessedPolitician():
	with app.app_context():
		# Go to the database, order the tweets on some created column, and
		# return the associated politician for that entry.
		last_tweet = Tweet.query.order_by(Tweet.id.desc()).limit(1).first()
		last_politician_processed = last_tweet.query_term
		return last_politician_processed

# Rearchitecture (01/29/24):
# Do / process one of the politicians at a time.
# Rearchitecture (02/28/24):
# Just keep it as simple as possible (like KISS on steroids)
def masterUpdateMethod():
	with app.app_context():
		# Every hour lets say, do the following:
		# (1) Getting the list of politicians
		politicians = [
			'Joe Biden', 'Marianne Williamson', 'Dean Phillips',
			'Donald Trump', 'Nikki Haley', 'Vivek Ramaswamy', 'Asa Hutchinson',
			'Ron DeSantis', 'Chris Christie'
		]

		# last_politician_processed = getLastProcessedPolitician()
		# last_politician_processed_index = (politicians.index(last_politician_processed) + 1) % len(politicians)

		# (2) Looping through each one, querying the Twitter via Nitter. Store in an object.
		for politician in politicians:
			my_sentiment_analyzer.setQueryTerm(politician)
			politician_sentiment_data = {}
			tweets = my_twitter_scraper.getTweetsForQuery(politician, 100)
			politician_sentiment_data[politician] = []
			for tweet in tweets:
				try:
					sentiment = my_sentiment_analyzer.getSentimentForTweet(tweet['text'])
					# print('Politician = ' + politician + ', Tweet = ' + tweet['text'] + ', Sentiment = ' + sentiment)
					politician_sentiment_data[politician].append({
						'tweet': tweet['text'], 'sentiment': sentiment
					})
				except Exception as e:
					print(e)
					continue
		# (3) Keeping track of those tweets in our database, along with the derived sentiments. Process the
		# object made above.
		# [01-16-24] Changed to only wiriting a single politician's data to the DB at one time to optimize for memory usage.
		print('[DEBUG] BEFORE CALL TO loadAllSentimentDistributions for politician = ' + politician)
		commands.loadAllSentimentDistributions(politician_sentiment_data)
		print('[DEBUG] AFTER CALL TO loadAllSentimentDistributions for politician = ' + politician)
		# print('[DEBUG] BEFORE CALL TO masterGeographicSentimentAnalyzer')
		# masterGeographicSentimentAnalyzer()
		# print('[DEBUG] AFTER CALL TO masterGeographicSentimentAnalyzer')
		# The rest of the stuff the Frontend / UI should take care of.
		# tokenizer_minify('cardiffnlp/twitter-roberta-base-sentiment', 15000, 'twitter-roberta-minified-15k')	

db_update_scheduler = BackgroundScheduler()
# It'll be run once right away when the script is first started
politicians = [
	'Joe Biden', 'Marianne Williamson', 'Dean Phillips',
	'Donald Trump', 'Nikki Haley', 'Vivek Ramaswamy', 'Asa Hutchinson',
	'Ron DeSantis', 'Chris Christie'
]

db_update_scheduler.add_job(func=masterUpdateMethod, trigger="interval", seconds=7200)
db_update_scheduler.add_job(func=masterUpdateMethod, trigger="date", run_date=datetime.datetime.now())
# db_update_scheduler.add_job(func=masterUpdateMethod, args=[politicians[0]], trigger="date", run_date=datetime.datetime.now(), name='masterUpdateMethod', id='masterUpdateMethod-' + politicians[0])
# db_update_scheduler.add_job(func=masterGeographicSentimentAnalyzer,trigger="date", run_date=datetime.datetime.now(), name='masterGeographicSentimentAnalyzer', id='masterGeographicSentimentAnalyzer')
# Start the next instance of the job once the current instance completes
'''def my_listener_master_update(event):	
	if event.exception:
		print('The job has crashed with exception = ' + str(event.exception))
		db_update_scheduler.add_job(
			func=masterUpdateMethod,
			args=[politicians[0]],
			trigger="date",
			run_date=datetime.datetime.now(),
			name='masterUpdateMethod',
			id='masterUpdateMethod-' + politicians[0]
		)
	else:
		processed_politician = event.job_id.split('-')[1]
		print('\nprocessed_politician= ' + str(processed_politician) + '\n')
		next_politician = politicians[(politicians.index(processed_politician) + 1) % len(politicians)]
		db_update_scheduler.add_job(
			func=masterUpdateMethod,
			args=[next_politician],
			trigger="date",
			run_date=datetime.datetime.now(),
			name='masterUpdateMethod',
			id='masterUpdateMethod-' + next_politician
		)

def my_listener_master_geographic_sentiment_analyzer(event):
	if event.name == 'masterGeographicSentimentAnalyzer':
		if event.exception:
			print('The job has crashed with exception = ' + str(event.exception))
			db_update_scheduler.add_job(
				func=masterGeographicSentimentAnalyzer,
				trigger="date",
				run_date=datetime.datetime.now(),
				name='masterGeographicSentimentAnalyzer',
				id='masterGeographicSentimentAnalyzer'
			)
		else:
			db_update_scheduler.add_job(
				func=masterGeographicSentimentAnalyzer,
				trigger="date",
				run_date=datetime.datetime.now(),
				name='masterGeographicSentimentAnalyzer',
				id='masterGeographicSentimentAnalyzer'
			)
'''

# db_update_scheduler.add_listener(my_listener_master_update, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
# db_update_scheduler.add_listener(my_listener_master_geographic_sentiment_analyzer, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
# db_update_scheduler.add_job(func=masterUpdateMethod, trigger="interval", seconds=7200)
# Shut down the scheduler when exiting the app
# atexit.register(lambda: db_update_scheduler.shutdown())
# Explicitly starting the job in the background thread
# 01-10-24: Moving scheduler.start() to the bottom of __init__.py according to
# https://github.com/viniciuschiele/flask-apscheduler/issues/147
db_update_scheduler.start()

# Adding logging to find out wtf is going on with the frozen jobs
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

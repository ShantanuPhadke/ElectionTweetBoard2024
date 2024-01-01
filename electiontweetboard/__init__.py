from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# For Background Scheduling
import datetime
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

from electiontweetboard.tokenizers.tokenizer_utils import tokenizer_minify

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])
app.config['SECRET_KEY'] = 'secret_key'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://snwmumshcsdhgd:63d1821b97e3e24111e9d36e496538ea0147c55db5ad52f5a7ed6357a8196c3d@ec2-3-217-146-37.compute-1.amazonaws.com:5432/dv41rc55lk3kl';
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)

from electiontweetboard import routes, commands
# Our TwitterConnection and VaderWrapper Singletons of course
from electiontweetboard.data.TwitterScraper import TwitterScraper
from electiontweetboard.nlp.SentimentAnalyzer import SentimentAnalyzer

# Our actual TwitterConnection and VADER Wrapper objects
my_twitter_scraper = TwitterScraper.getInstance()
my_sentiment_analyzer = SentimentAnalyzer.getInstance()

def masterUpdateMethod():
    '''
    # Every hour lets say, do the following:
    # (1) Getting the list of politicians
    politicians = [
        'Joe Biden', 'Marianne Williamson', 'Dean Phillips',
        'Donald Trump', 'Nikki Haley', 'Vivek Ramaswamy', 'Asa Hutchinson',
        'Ron DeSantis', 'Chris Christie'
    ]

    # (2) Looping through each one, querying the Twitter via Nitter. Store in an object.
    all_politician_sentiment_data = {}
    for politician in politicians:
        tweets = my_twitter_scraper.getTweetsForQuery(politician, 50)
        all_politician_sentiment_data[politician] = []
        for tweet in tweets:
            try:
                sentiment = my_sentiment_analyzer.getSentimentForTweet(tweet['text'])
                # print('Politician = ' + politician + ', Tweet = ' + tweet['text'] + ', Sentiment = ' + sentiment)
                all_politician_sentiment_data[politician].append({
                    'tweet': tweet['text'], 'sentiment': sentiment
                })
            except:
                continue
        # print('politician = ' + politician + ', all_politician_sentiment_data[politician] = ' + str(all_politician_sentiment_data[politician]))
    # (3) Keeping track of those tweets in our database, along with the derived sentiments. Process the
    # object made above.
    with app.app_context():
        commands.loadAllSentimentDistributions(all_politician_sentiment_data)

    # The rest of the stuff the Frontend / UI should take care of.
    '''
    tokenizer_minify('cardiffnlp/twitter-roberta-base-sentiment', 5000, 'twitter-roberta-minified')

db_update_scheduler = BackgroundScheduler()
# It'll be run once right away when the script is first started
db_update_scheduler.add_job(func=masterUpdateMethod,trigger="date", run_date=datetime.datetime.now())
# It'll be scheduled once every hour
db_update_scheduler.add_job(func=masterUpdateMethod, trigger="interval", seconds=7200)
# Explicitly starting the job in the background thread
db_update_scheduler.start()
# Shut down the scheduler when exiting the app
atexit.register(lambda: db_update_scheduler.shutdown())

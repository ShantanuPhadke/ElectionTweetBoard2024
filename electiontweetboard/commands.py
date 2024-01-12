from electiontweetboard import app, db
from electiontweetboard.models import Tweet, SentimentDistribution, SentimentsOverTime, StateSentiment, QuickLink
from electiontweetboard.links.LinkExtractor import LinkExtractor

import datetime

my_link_extractor = LinkExtractor()

def loadStateSentimentDistribution(query_term, state_symbol, negative_percent, neutral_percent, positive_percent):
	old_state_sentiment_distribution = StateSentiment.query.filter_by(query_term=query_term, state_symbol=state_symbol).all()
	state_sentiment_distribution_obj = StateSentiment(
			query_term=query_term,
			state_symbol=state_symbol,
			positive_percent=positive_percent,
			negative_percent=negative_percent,
			neutral_percent=neutral_percent
		)
	db.session.add(state_sentiment_distribution_obj)
	db.session.commit()
	StateSentiment.query.filter_by(id=old_state_sentiment_distribution[0].id).delete()
	db.session.commit()

def loadAllSentimentDistributions(all_politician_sentiment_data):
	all_politician_sentiment_distributions = {}
	all_politician_tweets_by_sentiment = {}
	all_politician_sample_tweets_by_sentiment = {}
	num_sample_tweets = 12
	# A. For each politician:
	for politician in all_politician_sentiment_data:
		# 1. Get the old data
		old_tweets = Tweet.query.filter_by(query_term=politician).all()
		old_sentiment_distributions = SentimentDistribution.query.filter_by(query_term=politician).all()
		old_sentiments_over_times = SentimentsOverTime.query.filter_by(query_term=politician).all()
		old_quick_links = QuickLink.query.filter_by(query_term=politician).all()

		all_politician_sentiment_distributions[politician] = {
			'negative_sentiment_percent': 0, 'positive_sentiment_percent': 0, 'neutral_sentiment_percent': 0,
		}
		all_politician_tweets_by_sentiment[politician] = {
			'negative_sentiment_tweets': [], 'neutral_sentiment_tweets': [], 'positive_sentiment_tweets': [],
		}
		all_politician_sample_tweets_by_sentiment[politician] = {
			'negative_sentiment_tweets': [], 'neutral_sentiment_tweets': [], 'positive_sentiment_tweets': [],
		}

		num_positive = 0.0
		num_neutral = 0.0
		num_negative = 0.0

		for tweet_data in all_politician_sentiment_data[politician]:
			tweet = tweet_data['tweet']
			sentiment = tweet_data['sentiment']

			# 2. Get the sentiment distributions (% Negative, % Neutral, % Positive) for the current politician.
			if sentiment == 'Positive':
				all_politician_sample_tweets_by_sentiment[politician]['positive_sentiment_tweets'].append(tweet)
				if num_positive < num_sample_tweets:
					tweet_obj = Tweet(tweet=tweet, query_term=politician, sentiment=sentiment)
					db.session.add(tweet_obj)
				num_positive += 1
			elif sentiment == 'Neutral':
				all_politician_sample_tweets_by_sentiment[politician]['neutral_sentiment_tweets'].append(tweet)
				if num_neutral < num_sample_tweets:
					tweet_obj = Tweet(tweet=tweet, query_term=politician, sentiment=sentiment)
					db.session.add(tweet_obj)
				num_neutral += 1
			else:
				all_politician_sample_tweets_by_sentiment[politician]['negative_sentiment_tweets'].append(tweet)
				if num_negative < num_sample_tweets:
					tweet_obj = Tweet(tweet=tweet, query_term=politician, sentiment=sentiment)
					db.session.add(tweet_obj)
				num_negative += 1
		
			# 3. Loop through the relevant tweets + extract any relevant links
			link = my_link_extractor.extract_link(tweet)
			if link:
				link_info = my_link_extractor.analyze_link(link, politician)
				# print('link_info = ' + str(link_info))
				if link_info != 'SPAM LINK LIKELY!':
					quick_link_obj = QuickLink(query_term=politician, link=link, title=link_info)
					db.session.add(quick_link_obj)

		db.session.commit()

		# 4. Update the SentimentsDistribution / SentimentsOverTime for the current politician.
		num_total = len(all_politician_sentiment_data[politician])
		sentiments_distribution_obj = SentimentDistribution(
			query_term=politician,
			positive_percent=(num_positive/num_total)*100,
			negative_percent=(num_negative/num_total)*100,
			neutral_percent=(num_neutral/num_total)*100
		)
		db.session.add(sentiments_distribution_obj)
		db.session.commit()

		current_timestamp = datetime.datetime.now()
		today = str(current_timestamp).split(" ")[0]
		sentiments_over_time_today = SentimentsOverTime.query.filter_by(timestamp=today).filter_by(query_term=politician).first()
		if not sentiments_over_time_today:
			sentiments_over_time_obj = SentimentsOverTime(
				query_term=politician,
				timestamp=today,
				positive_percent=(num_positive/num_total)*100,
				negative_percent=(num_negative/num_total)*100,
				neutral_percent=(num_neutral/num_total)*100
			)
			db.session.add(sentiments_over_time_obj)
			db.session.commit()

		# 5. Delete the old data
		for old_tweet in old_tweets:
			Tweet.query.filter_by(id=old_tweet.id).delete()
		db.session.commit()

		for old_sentiment_distribution in old_sentiment_distributions:
			SentimentDistribution.query.filter_by(id=old_sentiment_distribution.id).delete()
		db.session.commit()

		for old_quick_link in old_quick_links:
			QuickLink.query.filter_by(id=old_quick_link.id).delete()
		db.session.commit()
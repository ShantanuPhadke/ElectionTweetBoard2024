import flask
from flask import jsonify

from electiontweetboard import app
from electiontweetboard.models import Tweet, SentimentDistribution, SentimentsOverTime, QuickLink, StateSentiment

from collections import Counter

@app.route("/")
def myIndex():
	return flask.render_template("index.html", token="Hello Flask+React")

@app.route("/democrats")
def myIndexDemocrats():
	return flask.render_template("index.html", token="Hello Flask+React")

@app.route("/republicans")
def myIndexRepublicans():
	return flask.render_template("index.html", token="Hello Flask+React")

@app.route("/democrats/<candidate_name>/quick-links-modal")
def myIndexDemocratsQuickLinksModal(candidate_name):
	return flask.render_template("index.html", token="Hello Flask+React")

@app.route("/republicans/<candidate_name>/quick-links-modal")
def myIndexRepublicansQuickLinksModal(candidate_name):
	return flask.render_template("index.html", token="Hello Flask+React")

@app.route("/democrats/<candidate_name>/tweets-modal/sample-tweets")
def myIndexDemocratsTweetsModalSampleTweets(candidate_name):
	return flask.render_template("index.html", token="Hello Flask+React")

@app.route("/republicans/<candidate_name>/tweets-modal/sample-tweets")
def myIndexRepublicansTweetsModalSampleTweets(candidate_name):
	return flask.render_template("index.html", token="Hello Flask+React")

@app.route("/democrats/<candidate_name>/tweets-modal/sentiments-over-time/one-day")
def myIndexDemocratsTweetsModalSentimentsOverTimeOneDay(candidate_name):
	return flask.render_template("index.html", token="Hello Flask+React")

@app.route("/democrats/<candidate_name>/tweets-modal/sentiments-over-time/one-week")
def myIndexDemocratsTweetsModalSentimentsOverTimeOneWeek(candidate_name):
	return flask.render_template("index.html", token="Hello Flask+React")

@app.route("/democrats/<candidate_name>/tweets-modal/sentiments-over-time/one-month")
def myIndexDemocratsTweetsModalSentimentsOverTimeOneMonth(candidate_name):
	return flask.render_template("index.html", token="Hello Flask+React")

@app.route("/democrats/<candidate_name>/tweets-modal/sentiments-over-time/max")
def myIndexDemocratsTweetsModalSentimentsOverTimeMax(candidate_name):
	return flask.render_template("index.html", token="Hello Flask+React")

@app.route("/republicans/<candidate_name>/tweets-modal/sentiments-over-time/one-day")
def myIndexRepublicansTweetsModalSentimentsOverTimeOneDay(candidate_name):
	return flask.render_template("index.html", token="Hello Flask+React")

@app.route("/republicans/<candidate_name>/tweets-modal/sentiments-over-time/one-week")
def myIndexRepublicansTweetsModalSentimentsOverTimeOneWeek(candidate_name):
	return flask.render_template("index.html", token="Hello Flask+React")

@app.route("/republicans/<candidate_name>/tweets-modal/sentiments-over-time/one-month")
def myIndexRepublicansTweetsModalSentimentsOverTimeOneMonth(candidate_name):
	return flask.render_template("index.html", token="Hello Flask+React")

@app.route("/republicans/<candidate_name>/tweets-modal/sentiments-over-time/max")
def myIndexRepublicansTweetsModalSentimentsOverTimeMax(candidate_name):
	return flask.render_template("index.html", token="Hello Flask+React")

@app.route("/democrats/<candidate_name>/tweets-modal/sentiments-by-geography")
def myIndexDemocratsTweetsModalSentimentsByGeography(candidate_name):
	return flask.render_template("index.html", token="Hello Flask+React")

@app.route("/republicans/<candidate_name>/tweets-modal/sentiments-by-geography")
def myIndexRepublicansTweetsModalSentimentsByGeography(candidate_name):
	return flask.render_template("index.html", token="Hello Flask+React")

@app.route('/get_latest_sentiments/<query_string>', methods=['GET'])
def getLatestSentiments(query_string):
	relevant_distribution = SentimentDistribution.query.filter_by(query_term=query_string).first()
	if relevant_distribution:
		return jsonify(negative_sentiment_percent=int(round(relevant_distribution.negative_percent)),
					positive_sentiment_percent=int(round(relevant_distribution.positive_percent)),
					neutral_sentiment_percent=int(round(relevant_distribution.neutral_percent)))
	return jsonify(negative_sentiment_percent=0,
					positive_sentiment_percent=0,
					neutral_sentiment_percent=100)

@app.route('/get_latest_tweets/<query_string>')
def getLatestTweets(query_string):
	if len(query_string) > 0 and query_string != "none":
		relevant_negative_tweets = Tweet.query.filter_by(sentiment="Negative").filter_by(query_term=query_string).all()
		#relevant_neutral_tweets = SampleTweets.query.filter_by(query_term=query_string).first()
		relevant_positive_tweets = Tweet.query.filter_by(sentiment="Positive").filter_by(query_term=query_string).all()
		if relevant_negative_tweets and relevant_positive_tweets:
			return jsonify(negative_tweets_sample=[relevant_negative_tweet.tweet for relevant_negative_tweet in relevant_negative_tweets],
						positive_tweets_sample=[relevant_positive_tweet.tweet for relevant_positive_tweet in relevant_positive_tweets])

	return jsonify(negative_tweets_sample="Default Negative Sample",
					neutral_tweets_sample="Default Neutral Sample",
					positive_tweets_sample="Default Positive Sample")

@app.route('/get_sentiment_snapshots/<query_string>')
def getSentimentSnapshot(query_string):
	sentiment_snapshots = SentimentsOverTime.query.filter_by(query_term=query_string).all()
	positive_percents_over_time = {"name": "Positive Sentiment"}
	positive_sentiments_over_time = {}

	neutral_percents_over_time = {"name": "Neutral Sentiment"}
	neutral_sentiments_over_time = {}

	negative_percents_over_time = {"name": "Negative Sentiment"}
	negative_sentiments_over_time = {}

	for sentiment_snapshot in sentiment_snapshots:
		positive_sentiments_over_time[sentiment_snapshot.timestamp] = sentiment_snapshot.positive_percent
		neutral_sentiments_over_time[sentiment_snapshot.timestamp] = sentiment_snapshot.neutral_percent
		negative_sentiments_over_time[sentiment_snapshot.timestamp] = sentiment_snapshot.negative_percent

	positive_percents_over_time["data"] = positive_sentiments_over_time
	neutral_percents_over_time["data"] = neutral_sentiments_over_time
	negative_percents_over_time["data"] = negative_sentiments_over_time

	return jsonify(sentiment_time_data=[positive_percents_over_time, 
										neutral_percents_over_time,
										negative_percents_over_time])

@app.route('/get_sorted_ordering/<party>/<order_type>')
def getSortedOrdering(party, order_type):
	# Bucketed politicians
	all_politicians = {"Republicans": ["Donald Trump", "Nikki Haley", "Vivek Ramaswamy", "Asa Hutchinson", "Ron DeSantis", "Chris Christie"],
						"Democrats": ["Joe Biden", "Marianne Williamson", "Dean Phillips"]}
	dim = 150
	politicianToInfoMapping = {
		"Joe Biden": {
			"id": 1,
			"initials": "JB",
			"name": "Joe Biden",
			"imageSrc": "https://upload.wikimedia.org/wikipedia/commons/a/ad/Joe_Biden_%2848548455397%29_%28rotated%29.jpg",
			"imageHeight": dim,
			"imageWidth": dim,
			"linkSrc": "https://commons.wikimedia.org/wiki/File:Joe_Biden_(48548455397)_(rotated).jpg",
			"linkSrcExtraInfo": "Gage Skidmore from Peoria, AZ, USA",
			"runningStatus": True,
			"dropOutDate": ""
		},
		"Marianne Williamson": {
			"id": 2,
			"initials": "MW",
			"name": "Marianne Williamson",
			"imageSrc": "https://upload.wikimedia.org/wikipedia/commons/8/83/Marianne_Williamson_Profile.jpg",
			"imageHeight": dim,
			"imageWidth": dim,
			"linkSrc": "https://commons.wikimedia.org/wiki/File:Marianne_Williamson_Profile.jpg",
			"linkSrcExtraInfo": "Supearnesh [CC BY-SA 4.0]",
			"runningStatus": True,
			"dropOutDate": ""
		},
		"Dean Phillips":{
			"id": 3,
			"initials": "DP",
			"name": "Dean Phillips",
			"imageSrc": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Dean_Phillips%2C_official_portrait%2C_116th_Congress.jpg",
			"imageHeight": dim,
			"imageWidth": dim,
			"linkSrc": "https://commons.wikimedia.org/wiki/File:Dean_Phillips,_official_portrait,_116th_Congress.jpg",
			"linkSrcExtraInfo": "Eric Connolly - phillips.house.gov",
			"runningStatus": True,
			"dropOutDate": ""
		},
		"Donald Trump":{
			 "id": 4,
			"initials": "DT",
			"name": "Donald Trump",
			"imageSrc": "https://upload.wikimedia.org/wikipedia/commons/5/53/Donald_Trump_official_portrait_%28cropped%29.jpg",
			"imageHeight": dim,
			"imageWidth": dim,
			"linkSrc": "https://commons.wikimedia.org/wiki/File:Donald_Trump_official_portrait_(cropped).jpg",
			"linkSrcExtraInfo": "Shealah Craighead [Public domain]",
			"runningStatus": True,
			"dropOutDate": ""
		},
		 "Nikki Haley": {
			"id": 5,
			"initials": "NH",
			"name": "Nikki Haley",
			"imageSrc": "https://upload.wikimedia.org/wikipedia/commons/5/53/Nikki_Haley_2023_%28cropped%29.jpg",
			"imageHeight": dim,
			"imageWidth": dim,
			"linkSrc": "https://commons.wikimedia.org/wiki/File:Nikki_Haley_2023_(cropped).jpg",
			"linkSrcExtraInfo": "Gage Skidmore from Surprise, AZ, United States of America",
			"runningStatus": True,
			"dropOutDate": ""
		},
		 "Vivek Ramaswamy": {
			"id": 6,
			"initials": "VR",
			"name": "Vivek Ramaswamy",
			"imageSrc": "https://upload.wikimedia.org/wikipedia/commons/9/96/Vivek_Ramaswamy_by_Gage_Skidmore.jpg",
			"imageHeight": dim,
			"imageWidth": dim,
			"linkSrc": "https://commons.wikimedia.org/wiki/File:Vivek_Ramaswamy_by_Gage_Skidmore.jpg",
			"linkSrcExtraInfo": "Gage Skidmore from Surprise, AZ, United States of America",
			"runningStatus": True,
			"dropOutDate": ""
		},
		 "Asa Hutchinson": {
			"id": 7,
			"initials": "AH",
			"name": "Asa Hutchinson",
			"imageSrc": "https://upload.wikimedia.org/wikipedia/commons/6/69/Asa_Hutchinson_by_Gage_Skidmore.jpg",
			"imageHeight": dim,
			"imageWidth": dim,
			"linkSrc": "https://commons.wikimedia.org/wiki/File:Asa_Hutchinson_by_Gage_Skidmore.jpg",
			"linkSrcExtraInfo": "Gage Skidmore from Surprise, AZ, United States of America",
			"runningStatus": True,
			"dropOutDate": ""
		},
		"Ron DeSantis": {
			 "id": 8,
			"initials": "RD",
			"name": "Ron DeSantis",
			"imageSrc": "https://upload.wikimedia.org/wikipedia/commons/f/f1/Ron_DeSantis_in_October_2023.jpg",
			"imageHeight": dim,
			"imageWidth": dim,
			"linkSrc": "https://commons.wikimedia.org/wiki/File:Ron_DeSantis_in_October_2023.jpg",
			"linkSrcExtraInfo": "Gage Skidmore from Surprise, AZ, United States of America",
			"runningStatus": True,
			"dropOutDate": ""
		},
		"Chris Christie":{
			"id": 9,
			"initials": "CC",
			"name": "Chris Christie",
			"imageSrc": "https://upload.wikimedia.org/wikipedia/commons/7/72/Chris_Christie_%2853297980082%29_%28cropped%29.jpg",
			"imageHeight": dim,
			"imageWidth": dim,
			"linkSrc": "https://commons.wikimedia.org/wiki/File:Chris_Christie_(53297980082)_(cropped).jpg",
			"linkSrcExtraInfo": "Gage Skidmore from Surprise, AZ, United States of America",
			"runningStatus": True,
			"dropOutDate": ""
		}
	}
	if order_type == 'positive_percent':
		relevant_ordering = SentimentDistribution.query.order_by(SentimentDistribution.positive_percent).all()[::-1]
	elif order_type == 'neutral_percent':
		relevant_ordering = SentimentDistribution.query.order_by(SentimentDistribution.neutral_percent).all()[::-1]
	else:
		relevant_ordering = SentimentDistribution.query.order_by(SentimentDistribution.negative_percent).all()[::-1]
	ordering = [politicianToInfoMapping[entry.query_term] for entry in relevant_ordering if entry.query_term in all_politicians[party]]
	return jsonify(order=ordering)

@app.route('/get_current_links/<query_term>')
def getCurrentLinks(query_term):
	query_term_links = QuickLink.query.filter_by(query_term=query_term).all()
	relevant_links = [(query_term_link.link,query_term_link.title) for query_term_link in query_term_links]
	relevant_titles = [query_term_link.title for query_term_link in query_term_links]
	title_counter = Counter(relevant_titles)
	num_links = min(25, len(title_counter.items()))

	unique_relevant_link_infos = []
	title_counter_dict = dict(title_counter)

	for relevant_link_info in relevant_links:
		if relevant_link_info[1] in title_counter_dict:
			unique_relevant_link_infos.append(relevant_link_info)
			# Delete the relevant link title whose relevant link info we just added in
			del title_counter_dict[relevant_link_info[1]]

	link_counter = Counter(unique_relevant_link_infos)
	most_common_links = link_counter.most_common(num_links)

	# Current makeshift way of filtering out potentially "spamming links"
	# Take the average number of occurrences of the top links
	# if any link has > 2*average number of top link occurrences, remove it
	# from our list (it is likely spammy)

	return jsonify(links=most_common_links)

@app.route('/get_all_state_sentiments/<query_string>')
def getAllStateSentiments(query_string):
	all_state_scores = {}
	state_sentiments = StateSentiment.query.filter_by(query_term=query_string).all()
	print("State Sentiments Found: " + str(state_sentiments))
	for state_sentiment in state_sentiments:
		state_sentiment = state_sentiment
		state_score = state_sentiment.positive_percent + state_sentiment.neutral_percent
		all_state_scores[state_sentiment.state_symbol] = state_score
	return jsonify(state_scores=all_state_scores)
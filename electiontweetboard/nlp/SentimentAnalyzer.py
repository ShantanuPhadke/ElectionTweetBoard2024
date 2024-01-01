from transformers import AutoTokenizer, PreTrainedTokenizerFast, AutoModelForSequenceClassification
from scipy.special import softmax

class SentimentAnalyzer:
	# This will represent the one and only 'true' Twitter Connection 
	# for our application.
	_instance = None

	@staticmethod
	def getInstance():
		# This is where we return our instance :)
		if SentimentAnalyzer._instance == None:
			SentimentAnalyzer()
		return SentimentAnalyzer._instance
	
	# ATTENTION: This is now a private constructor, if we want to
	# define a SentimentAnalyzer object outside of this SentimentAnalyzer
	# class from now on, we will have to use SentimentAnalyzer.getInstance()
	def __init__(self):
		if SentimentAnalyzer._instance != None:
			raise Exception("Derp de Herp Herp! SentimentAnalyzer is a singleton mate!")
		else:
			SentimentAnalyzer._instance = self
	
	def setQueryTerm(self, query_term):
		self.query_term = query_term

	def getSentimentForTweet(self, tweet):
		tweet_words = []
		for word in tweet.split(' '):
			if word.startswith('@') and len(word) > 1:
				word = '@user'
			elif word.startswith('http'):
				word = 'http'
			tweet_words.append(word)

		tweet_processed = ' '.join(tweet_words)
		print('tweet_processed = ' + str(tweet_processed))
		roberta = "cardiffnlp/twitter-roberta-base-sentiment"
		model = AutoModelForSequenceClassification.from_pretrained(roberta)
		# tokenizer = AutoTokenizer.from_pretrained(roberta)
		tokenizer = PreTrainedTokenizerFast(tokenizer_file="twitter-roberta-unified/tokenizer.json")
		tokenizer.model_max_length = 512
		tokenizer.padding = 'max_length'
		tokenizer.truncation = True
		labels = ['Negative', 'Neutral', 'Positive']
		# actual sentiment analysis
		encoded_tweet = tokenizer(tweet_processed, return_tensors='pt')
		print('encoded_tweet = ' + str(encoded_tweet))
		output = model(**encoded_tweet)
		scores = output[0][0].detach().numpy()
		scores = softmax(scores)
		print('scores = ' + str(scores))
		max_score = 0
		max_score_label = None

		for i in range(len(scores)):
			l = labels[i]
			s = scores[i]

			if s > max_score:
				max_score = s
				max_score_label = l
		
		#print('Tweet = ' + first_tweet_text)
		#print('Label = ' + max_score_label)
		#print('Probability = ' + str(max_score))
		print("max_score_label = " + str(max_score_label) + ', max_score = ' + str(max_score))
		return max_score_label
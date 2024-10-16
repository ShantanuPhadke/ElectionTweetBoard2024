from transformers import AutoTokenizer, PreTrainedTokenizerFast, AutoModelForSequenceClassification
from scipy.special import softmax
import os

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
			project_dir = os.path.dirname(__file__)
			roberta = "cardiffnlp/twitter-roberta-base-sentiment"
			absa = "yangheng/deberta-v3-base-absa-v1.1"
			# SentimentAnalyzer.tokenizer = AutoTokenizer.from_pretrained(roberta)
			SentimentAnalyzer.absa_tokenizer = AutoTokenizer.from_pretrained(absa, use_fast=False)
			# SentimentAnalyzer.roberta_model = AutoModelForSequenceClassification.from_pretrained(roberta, low_cpu_mem_usage=True)
			SentimentAnalyzer.absa_model = AutoModelForSequenceClassification.from_pretrained(absa, low_cpu_mem_usage=True)
	
	def setQueryTerm(self, query_term):
		SentimentAnalyzer.query_term = query_term

	def getSentimentForTweet(self, tweet):
		tweet_words = []
		for word in tweet.split(' '):
			if word.startswith('@') and len(word) > 1:
				word = '@user'
			elif word.startswith('http'):
				word = 'http'
			tweet_words.append(word)

		tweet_processed = ' '.join(tweet_words)[:512]

		# model = SentimentAnalyzer.roberta_model
		# encoded_tweet = SentimentAnalyzer.tokenizer(tweet_processed, return_tensors='pt', truncation=True, max_length=512)
		# if SentimentAnalyzer.query_term in tweet:
		model = SentimentAnalyzer.absa_model
		encoded_tweet = SentimentAnalyzer.absa_tokenizer(tweet_processed, SentimentAnalyzer.query_term, return_tensors='pt', truncation=True, max_length=512)

		labels = ['Negative', 'Neutral', 'Positive']
		output = model(**encoded_tweet)
		scores = output[0][0].detach().numpy()
		scores = softmax(scores)
		max_score = 0
		max_score_label = None

		for i in range(len(scores)):
			l = labels[i]
			s = scores[i]

			if s > max_score:
				max_score = s
				max_score_label = l
		
		return max_score_label
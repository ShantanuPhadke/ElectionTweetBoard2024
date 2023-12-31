import urllib3
from bs4 import BeautifulSoup

class LinkExtractor:
	# This will represent the one and only 'true' Twitter Connection 
	# for our application.
	_instance = None

	@staticmethod
	def getInstance():
		# This is where we return our instance :)
		if LinkExtractor._instance == None:
			LinkExtractor()
		return LinkExtractor._instance
	

	# ATTENTION: This is now a private constructor, if we want to
	# define a LinkExtractor object outside of this LinkExtractor
	# class from now on, we will have to use LinkExtractor.getInstance()
	def __init__(self):
		if LinkExtractor._instance != None:
			raise Exception("Derp de Herp Herp! LinkExtractor is a singleton mate!")
		else:
			LinkExtractor._instance = self

	def extract_link(self, current_tweet):
		link_index = current_tweet.find("https://")
		if link_index == -1:
			return None
		currentTweet = ' '.join(current_tweet.split())
		tweet_words = current_tweet.split(' ')
		for word in tweet_words:
			if word.find("https://") == 0:
				return word
		return None

	def extract_all_links(self, current_tweets):
		all_links = [self.extract_link(tweet) for tweet in current_tweets if self.extract_link(tweet)]
		return all_links

	def analyze_link(self, link, query_term):
		try: 
			# use headers for the forbidden errors
			headers = {"User-Agent": "Mozilla/5.0"}
			req = urllib3.request.Request(link, headers =headers)
			html = urllib3.request.urlopen(req)
			contentToProcess = urllib3.request.urlopen(req)
			htmlStr = str(html.read())

			if query_term not in htmlStr:
				firstName, lastName = query_term.split(' ')
				if firstName not in htmlStr and lastName not in htmlStr:
					return 'SPAM LINK LIKELY!'

			beginning = htmlStr[:2000]
			ending = htmlStr[len(htmlStr)-2000:]

			if 'html' in beginning and 'html' in ending:
				soup = BeautifulSoup(contentToProcess.read(), 'html.parser')
				currentTitle = str(soup.find('title'))
				if 'on Twitter:' in currentTitle:
					return currentTitle[7:].split(':')[0]
				currentTitle = currentTitle.split('>')[1]
				currentTitle = currentTitle.split('<')[0]
				return currentTitle
			else:
				return 'Audio Podcast'
		except Exception as e:
			return link



	
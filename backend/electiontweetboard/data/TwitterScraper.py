from ntscraper import Nitter

class TwitterScraper:
	# This will represent the one and only 'true' Twitter Connection 
	# for our application.
	_instance = None

	@staticmethod
	def getInstance():
		# This is where we return our instance :)
		if TwitterScraper._instance == None:
			TwitterScraper()
		return TwitterScraper._instance

	# ATTENTION: This is now a private constructor, if we want to
	# define a TwitterScraper object outside of this TwitterScraper
	# class from now on, we will have to use TwitterScraper.getInstance()
	def __init__(self):
		if TwitterScraper._instance != None:
			raise Exception("Derp de Herp Herp! TwitterScraper is a singleton mate!")
		else:
			TwitterScraper._instance = self

	def getTweetsForQuery(self, query_string, number_tweets):
		while True:
			try:
				scraper = Nitter()
				search_results = scraper.get_tweets(query_string, mode='term', number=number_tweets)
				if len(search_results['tweets']) > 0:
					break
				else:
					continue
			except:
				continue
		return search_results['tweets']
	
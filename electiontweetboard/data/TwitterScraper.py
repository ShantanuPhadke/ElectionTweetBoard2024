from ntscraper import Nitter
import multiprocessing

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
			TwitterScraper.scraper = None

	def handler(self, signum, frame):
		raise Exception("end of time")

	def getTweetsForQuery(self, query_string, number_tweets, near=None):
		if not TwitterScraper.scraper:
			TwitterScraper.scraper = Nitter(log_level=1)
		while True:
			print('IM IN THE LOOP!')
			try:
				search_results = TwitterScraper.scraper.get_tweets(query_string, mode='term', number=number_tweets, near=near, language='en')
				print('search_results = ' + str(search_results))
				if len(search_results['tweets']) > 0:
					break
				else:
					continue
			except Exception as e:
				print('\nException encountered in TwitterScraper!! e = ' + str(e) + '\n')
				continue
		return search_results['tweets']
	
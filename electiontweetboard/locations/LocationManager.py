class LocationManager:
	# This will represent the one and only 'true' Location Manager
	# for our application.
	_instance = None

	@staticmethod
	def getInstance():
		# This is where we return our instance :)
		if LocationManager._instance == None:
			LocationManager()
		return LocationManager._instance
	

	# ATTENTION: This is now a private constructor, if we want to
	# define a LocationManager object outside of this LocationManager
	# class from now on, we will have to use LocationManager.getInstance()
	def __init__(self):
		if LocationManager._instance != None:
			raise Exception("Derp de Herp Herp! LocationManager is a singleton mate!")
		else:
			default_radius = '75mi'
			LocationManager._instance = self
			LocationManager.all_states = {
				'CA': {
						'Los Angeles': (34.052,-118.2437,default_radius),
						'San Diego': (32.7157,-117.1611,default_radius),
						'San Jose': (32.3382,-121.8863,default_radius),
						'San Francisco': (37.7749,-122.4194,default_radius),
						'Fresno': (36.7378,-119.7871,default_radius)
					}, 
				'OR': {
						'Portland': (45.523,-122.676,default_radius),
						'Salem': (44.943,-123.035,default_radius),
						'Eugene': (44.052,-123.087,default_radius),
						'Gresham': (45.498,-122.431,default_radius),
						'Hillsboro': (45.523,-122.99,default_radius)
					}, 
				'WA': {
						'Seattle': (47.6062,-122.3321,default_radius),
						'Spokane': (47.6588,-117.4260,default_radius),
						'Tacoma': (47.2529,-122.4443,default_radius),
						'Vancouver': (49.2827,-123.1202,default_radius),
						'Bellevue': (47.6101,-122.2015,default_radius)
					}, 
				'AK': {
						'Anchorage': (61.2181,-149.9003,default_radius),
						'Juneau': (58.3019,-134.4197,default_radius),
						'Fairbanks': (64.8378,-147.7164,default_radius),
						'Wasilla': (61.5809,-149.4411,default_radius),
						'Sitka': (51.0531,-135.3300,default_radius)
					}, 
				'HI': {
						'Honolulu': (21.3069,-157.8583,default_radius),
						'East Honolulu': (21.2891,-157.7173,default_radius),
						'Pearl City': (21.3972,-157.9733,default_radius),
						'Hilo': (19.7274,-155.0868,default_radius),
						'Kailua': (21.4022,-157.7394,default_radius)
					},
				'AZ': {
						'Pheonix': (33.4484,-112.0740,default_radius),
						'Tuscon': (32.2226,-110.9747,default_radius),
						'Mesa': (33.4152,-111.8315,default_radius),
						'Chandler': (33.3062,-111.8413,default_radius),
						'Gilbert': (33.3528,-111.7840,default_radius)
					}, 
				'NM': {
						'Albuquerque': (35.0844,-106.6504,default_radius),
						'Las Cruces': (32.3199,-106.7637,default_radius),
						'Rio Rancho': (35.2328,-106.6630,default_radius),
						'Santa Fe': (35.6870,-105.9378,default_radius),
						'Roswell': (33.3943,-104.5230,default_radius)
					}, 
				'NV': {
						'Las Vegas': (36.1699,-115.1398,default_radius),
						'Henderson': (36.0395,-114.9817,default_radius),
						'Reno': (39.5296,-119.8138,default_radius),
						'North Las Vegas': (36.1989,-115.1175,default_radius),
						'Sparks': (39.5349,-119.7527,default_radius)
					},
				'UT': {
						'Salt Lake City': (40.7608,-111.8910,default_radius),
						'West Valley City': (40.6916,-112.0011,default_radius),
						'Provo': (40.2338,-111.6585,default_radius),
						'West Jordan': (40.6097,-111.9391,default_radius),
						'Orem': (40.2969,-111.6946,default_radius)
					}, 
				'ID': {
						'Boise': (43.6150,-116.3915,default_radius),
						'Meridian': (43.6121,-116.3915,default_radius),
						'Wampa': (43.5788,-116.5598,default_radius),
						'Idaho Falls': (43.4927,-112.0408,default_radius),
						'Potacello': (42.8621,-112.4506,default_radius)
					}, 
				'MT': {
						'Billings': (45.7833,-108.5007,default_radius),
						'Missoula': (46.8721,-113.9940,default_radius),
						'Great Falls': (47.5053,-111.3008,default_radius),
						'Bozeman': (45.6770,-111.0429,default_radius),
						'Butte': (46.0038,-112.5348,default_radius)
					}, 
				'WY': {
						'Cheyenne': (41.1400,-104.8202,default_radius),
						'Casper': (42.8501,-106.3252,default_radius),
						'Laramie': (41.3114,-105.5911,default_radius),
						'Gilette': (44.2911,-105.5022,default_radius),
						'Rock Springs': (41.5875,-109.2029,default_radius)
					},
				'CO': {
						'Denver': (39.7392,-104.9903,default_radius),
						'Colorado Springs': (38.8339,-104.8214,default_radius),
						'Aurora': (39.7294,-104.8319,default_radius),
						'Fort Collins': (40.5853,-105.0814,default_radius),
						'Lakewood': (39.7074,-105.0814,default_radius)
					},
				'TX': {
						'Houston': (29.7604,-95.3698,default_radius),
						'San Antonio': (29.4241,-98.4936,default_radius),
						'Dallas': (32.7767,-96.7970,default_radius),
						'Austin': (30.2672,-97.7431,default_radius),
						'Fort Worth': (32.7555,-97.3308,default_radius)
					}, 
				'ND': {
						'Fargo': (46.8772,-96.7898,default_radius),
						'Bismark': (46.8083,-100.7837,default_radius),
						'Grand Forks': (47.9253,-97.0329,default_radius),
						'Minot': (48.2330,-101.2923,default_radius),
						'West Fargo': (46.8769,-96.8999,default_radius)
					}, 
				'SD': {
						'Sioux Falls': (43.5473,-96.7283,default_radius),
						'Rapid City': (44.0805,-103.2310,default_radius),
						'Aberdeen': (45.4647,-98.4865,default_radius),
						'Brookings': (44.3114,-96.7984,default_radius),
						'Watertown': (44.8994,-97.1151,default_radius)
					}, 
				'NE': {
						'Omaha': (41.2565,-95.9345,default_radius),
						'Lincoln': (40.8136,-96.7026,default_radius),
						'Bellevue': (41.1544,-95.9146,default_radius),
						'Grand Island': (40.9264,-98.3420,default_radius),
						'Kearney': (40.6993,-99.0817,default_radius)
					},
				'MI': {
						'Detroit': (42.3314,-83.0458,default_radius),
						'Grand Rapids': (42.9634,-85.6681,default_radius),
						'Warren': (42.5145,-83.0147,default_radius),
						'Sterling Heights': (42.5803,-83.0302,default_radius),
						'Ann Arbor': (42.2808,-83.7430,default_radius)
					},
				'KY': {
						'Louisville/Jefferson': (38.2527,-85.7585,default_radius),
						'Lexington-Fayatte': (38.0406,-84.5037,default_radius),
						'Bowling-Green': (36.9685,-86.4808,default_radius),
						'Owensboro': (37.7719,-87.1112,default_radius),
						'Covington': (39.0837,-84.5086,default_radius)
					}, 
				'KS': {
						'Wichita': (37.6872,-97.3301,default_radius),
						'Overland': (38.9822,-94.6708,default_radius),
						'Kansas City': (39.1155,-94.6268,default_radius),
						'Olathe': (38.8814,-94.8191,default_radius),
						'Topeka': (39.0473,-95.6752,default_radius)
					}, 
				'OK': {
						'Oklahoma City': (35.4676,-97.5164,default_radius),
						'Tusla': (36.1540,-95.9928,default_radius),
						'Norman': (35.2226,-97.4395,default_radius),
						'Broken Arrow': (36.0609,-95.7975,default_radius),
						'Lawton': (34.6036,-98.3959,default_radius)
					}, 
				'LA': {	
						'New Orleans': (29.9511,-90.0715,default_radius),
						'Baton Rouge': (30.4515,-91.1871,default_radius),
						'Shreveport': (32.5252,-93.7502,default_radius),
						'Lafayette': (30.2241,-92.0198,default_radius),
						'Lake Charles': (30.2266,-93.2174,default_radius)
					}, 
				'AR': {
						'Little Rock': (34.7465,-92.2896,default_radius),
						'Fort Smith': (35.3859,-94.3985,default_radius),
						'Fayetteville': (36.0822,-94.1719,default_radius),
						'Springdale': (36.1867,-94.1288,default_radius),
						'Jonesboro': (35.8423,-90.7043,default_radius)
					}, 
				'MO': {
						'Kansas City': (39.0997,-94.5786,default_radius),
						'St. Louis': (38.6270,-90.1999,default_radius),
						'Springfield': (37.2090,-93.2923,default_radius),
						'Independence': (39.0911,-94.4115,default_radius),
						'Columbia': (38.9517,-92.3341,default_radius)
					}, 
				'IA': {
						'Des Moines': (41.5868,-93.6250,default_radius),
						'Cedar Rapids': (41.9779,-91.6656,default_radius),
						'Davenport': (41.5236,-90.5776,default_radius),
						'Sioux City': (42.4963,-96.4049,default_radius),
						'Iowa City': (41.6611,-91.5302,default_radius)
					},
				'IN': {
						'Evansville': (37.9716,87.5711,default_radius),
						'South Bend': (41.6764,-86.2520,default_radius),
						'Carmel': (39.9784,-86.1180,default_radius),
						'Fishers': (39.9568,-86.0134,default_radius),
						'Bloomington': (39.1653,-86.5264,default_radius)
					},
				'MN': {
						'Minneapolis': (44.9778,-93.2650,default_radius),
						'Saint Paul': (44.9537,-93.0900,default_radius),
						'Rochester': (44.0121,-92.4802,default_radius),
						'Duluth': (46.7867,-92.1005,default_radius),
						'Bloomington': (44.8408,-93.2483,default_radius)
					}, 
				'WI': {
						'Milwaukee': (43.0389,-87.9065,default_radius),
						'Madison': (43.0731,-89.4012,default_radius),
						'Green Bay': (39.0837,-84.5086,default_radius),
						'Kenosha': (42.5847,-87.8212,default_radius),
						'Racine': (42.7216,-87.7829,default_radius)
					}, 
				'IL': {
						'Chicago': (41.8781,-87.6298,default_radius),
						'Aurora': (41.7606,-88.3201,default_radius),
						'Rockford': (42.2711,-89.0940,default_radius),
						'Joliet': (41.525,-88.0817,default_radius),
						'Naperville': (41.7508,-88.1535,default_radius)
					}, 
				'TN': {
						'Nashville': (36.1627,-86.7876,default_radius),
						'Memphis': (35.1495,-90.0490,default_radius),
						'Knoxville': (35.9606,-83.9207,default_radius),
						'Chattanooga': (35.0456,-85.3097,default_radius),
						'Clarksville': (36.5298,-87.3595,default_radius)
					}, 
				'MS': {
						'Jackson': (32.2986,-90.1848,default_radius),
						'Gulfport': (30.3674,-89.0928,default_radius),
						'Southaven': (34.4919,-90.0023,default_radius),
						'Hattiesburg': (31.3271,-89.2903,default_radius),
						'Biloxi': (30.3960,-88.8853,default_radius)
					}, 
				'AL': {
						'Birmingham': (33.5186,-86.8104,default_radius),
						'Montgomery': (32.3792,-86.3077,default_radius),
						'Mobile': (30.6954,-88.0399,default_radius),
						'Huntsville': (34.7304,-86.5861,default_radius),
						'Tuscaloosa': (33.2098,-87.5692,default_radius)
					}, 
				'GA': {
						'Atlanta': (33.7490,-84.3880,default_radius),
						'Augusta': (33.4735,-82.0105,default_radius),
						'Columbus': (32.4922,-84.9403,default_radius),
						'Macon': (32.8407,-83.6324,default_radius),
						'Savannah': (32.0809,-81.0912,default_radius) 
					}, 
				'SC': {
						'Charleston': (32.7765,-79.9311,default_radius),
						'Columbia': (34.0007,-81.0348,default_radius),
						'North Charleston': (32.8771,-80.0131,default_radius),
						'Mount Pleasant': (32.8323,-79.8284,default_radius),
						'Rock Hill': (34.9249,-81.0251,default_radius)
					}, 
				'NC': {
						'Charlotte': (35.2271,-80.8431,default_radius),
						'Raleigh': (35.7796,-78.6382,default_radius),
						'Greensboro': (36.0728,-79.7920,default_radius),
						'Durham': (35.9940,-78.8986,default_radius),
						'Winston-Salem': (36.0999,-80.2442,default_radius)
					}, 
				'FL': {
						'Jacksonville': (30.3322,-81.6557,default_radius),
						'Miami': (25.7617,-80.1918,default_radius),
						'Tampa': (27.9506,-82.4572,default_radius),
						'Orlando': (28.5383,-81.3792,default_radius),
						'St. Petersburg': (27.7676,-82.6403,default_radius)
					}, 
				'VA': {
						'Virginia Beach': (36.8529,-75.9780,default_radius),
						'Norfolk': (36.8508,-76.2895,default_radius),
						'Chesapeake': (36.7682,-76.2875,default_radius),
						'Arlington': (38.8816,-77.0910,default_radius),
						'Richmond': (37.5407,-77.4360,default_radius)
					}, 
				'WV': {
						'Charleston': (38.3498,-81.6326,default_radius),
						'Huntington': (38.4192,-82.4452,default_radius),
						'Morgantown': (39.6295,-79.9559,default_radius),
						'Parkersburg': (39.2667,-81.5615,default_radius),
						'Wheeling': (40.0640,-80.7209,default_radius)
					}, 
				'OH': {
						'Columbus': (39.9612,-82.9988,default_radius),
						'Cleveland': (41.4993,-81.6944,default_radius),
						'Cincinnati': (39.1031,-84.5120,default_radius),
						'Toledo': (41.6528,-83.5379,default_radius),
						'Akron': (41.0814,-81.5190,default_radius)
					}, 
				'PA': {
						'Philadelphia': (39.9526,-75.1652,default_radius),
						'Pittsburgh': (40.4406,-79.9959,default_radius),
						'Allenstown': (40.6023,-75.4714,default_radius),
						'Erie': (42.1292,-80.0861,default_radius),
						'Reading': (40.3356,-75.9269,default_radius)
					}, 
				'NY': {
						'New York': (40.7178,-74.0060,default_radius),
						'Buffalo': (42.8864,-78.8784,default_radius),
						'Rochester': (43.15661,-72.6088,default_radius),
						'Yonkers': (40.9312,-73.8987,default_radius),
						'Syracuse': (43.0481,-76.1474,default_radius)
					},
				'MD': {
						'Baltimore': (39.2904,-76.6122,default_radius),
						'Columbia': (39.2037,-76.8610,default_radius),
						'Germantown': (39.1732,-77.2717,default_radius),
						'Silver Spring': (38.9907,-77.0261,default_radius),
						'Waldorf': (38.6265,-76.9105,default_radius)
					}, 
				'DE': {
						'Wilmington': (39.7447,-75.5484,default_radius),
						'Dover': (39.1582,-75.5244,default_radius),
						'Newark': (39.6837,-75.7497,default_radius),
						'Middletown': (39.4496,-75.7163,default_radius),
						'Smyrna': (39.2998,-75.6048,default_radius)
					}, 
				'NJ': {
						'Newark': (40.7357,-74.1724,default_radius),
						'Jersey City': (40.7178,-74.0431,default_radius),
						'Paterson': (40.9168,-74.1718,default_radius),
						'Elizabeth': (40.6640,-74.2107,default_radius),
						'Clifton': (40.8584,-74.1638,default_radius)
					}, 
				'CT': {
						'Bridgeport': (41.1792,-73.1894,default_radius),
						'New Haven': (41.3083,-72.9279,default_radius),
						'Stamford': (41.0534,-73.5387,default_radius),
						'Hartford': (41.7658,-72.6734,default_radius),
						'Waterburg': (41.5582,-73.0515,default_radius)
					}, 
				'RI': {
						'Providence': (41.8240,-71.4128,default_radius),
						'Cranston': (41.7798,-71.4373,default_radius),
						'Warwick': (41.7001,-71.4162,default_radius),
						'Pawtucket': (41.8787,-71.3826,default_radius),
						'East Providence': (41.8137,-71.3701,default_radius)
					}, 
				'MA': {
						'Boston': (42.3601,-71.0589,default_radius),
						'Worcester': (42.2626,-71.8023,default_radius),
						'Springfield': (42.1015,-72.5898,default_radius),
						'Lowell': (42.6334,-71.3162,default_radius),
						'Cambridge': (42.3736,-71.1097,default_radius)
					}, 
				'VT': {
						'Burlington': (44.4759,-73.2121,default_radius),
						'South Burlington': (44.467,-73.171,default_radius),
						'Rutland': (43.6106,-72.9726,default_radius),
						'Barre': (44.1970,-72.5020,default_radius),
						'Montpelier': (44.2601,-72.5754,default_radius)
					}, 
				'NH': {	
						'Machester': (42.9956,-71.4548,default_radius),
						'Nashua': (42.7654,-71.4676,default_radius),
						'Concord': (43.2081,-71.5376,default_radius),
						'Derry': (42.8806,-71.3273,default_radius),
						'Dover': (43.1979,-70.8737,default_radius)
					}, 
				'ME': {
						'Portland': (43.6591,-70.2568,default_radius),
						'Lewiston': (44.1004,-70.2148,default_radius),
						'Bangor': (44.8016,-68.7712,default_radius),
						'Auburn': (44.0979,-70.2312,default_radius),
						'South Portland': (43.6415,-70.2409,default_radius)
					}
		}

		for state in LocationManager.all_states:
			for city in LocationManager.all_states[state]:
				LocationManager.all_states[state][city] = self.changeLocationTupleToStr(
					LocationManager.all_states[state][city]
				)

	def changeLocationTupleToStr(self, location_tuple):
		latitude, longitude, radius = location_tuple
		return ','.join((str(latitude), str(longitude), radius))

	def getAllStatesInfo(self):
		return self.all_states
	